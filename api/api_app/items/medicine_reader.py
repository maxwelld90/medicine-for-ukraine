import pygsheets
import pandas as pd
from copy import deepcopy
import re
import warnings
import pickle
import zlib
import redis
import os

class CountryCodeError(Exception):
    pass

class RedisConnectionError(Exception):
    pass

class UnknownItemError(IndexError):
    pass

url_validator = re.compile(
        r'^(?:http|ftp)s?://' # http:// or https://
        r'(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+(?:[A-Z]{2,6}\.?|[A-Z0-9-]{2,}\.?)|' #domain...
        r'localhost|' #localhost...
        r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})' # ...or ip
        r'(?::\d+)?' # optional port
        r'(?:/?|[/?]\S+)$', re.IGNORECASE)

def is_valid_url(url):
    return re.match(url_validator, url) is not None

def select_country(df, country_code):
    '''
    df: a dataframe with a table (from our spreadsheet)
    country_code: ES, PL, etc.
    '''
    # Filter out all columns for other countries except "Name EN"
    columns_filtered = []
    for column in df.columns:
        if column != "Name EN" and column.startswith(('Name', 'Links')) and not column.endswith(country_code):
            continue
        columns_filtered.append(column)

    df_res = deepcopy(df[columns_filtered])
    return df_res

def split_and_filter_links(links_text):
    replacements = (',', '\n')
    for r in replacements:
        links_text = links_text.replace(r, ' ')
    res = links_text.split()
    return [link for link in res if is_valid_url(link)]

def get_links_for_item(df, country_code, item_index):
    '''
    df: a dataframe with a table from our spreadsheet, already filtered by country!
    country_code: ES, PL, ..
    item_index: number of the row in df that contains our item

    returns a list of valid links for buying the item
    '''
    country_codes = get_country_codes(df)
    if country_code not in country_codes:
        raise CountryCodeError(f'Country code not found: {country_code}')
    
    try:
        row = df.iloc[item_index]
    except IndexError:
        raise UnknownItemError(f'Item number {item_index} not found')

    links_cell = row['Links {0}'.format(country_code)]
    links_list = split_and_filter_links(links_cell)
    if not links_list:
        warnings.warn('No valid URLs found for this item!')
    return links_list

def get_language_codes(df):
    res = []
    for column in df.columns:
        if column.startswith('Name'):
            res.append(column.split()[-1]) # language code: last after whitespace
    return res

def get_country_codes(df):
    res = []
    for column in df.columns:
        if column.startswith('Links'):
            res.append(column.split()[-1]) # language code: last after whitespace
    return res

def get_items_list(df):
    index = list(df.index)
    lang_codes = get_language_codes(df)
    item_names_by_language = []
    for i in range(len(df)):
        new_entry = {}
        for code in lang_codes:
            new_entry[code] = df['Name '+code].iloc[i]
        item_names_by_language.append(new_entry)

    item_priorities = list(df['Priority'])
    res = []
    for i in range(len(index)):
        res.append({'row_number': index[i],
                    'item_names_by_language': item_names_by_language[i],
                    'is_high_priority': item_priorities[i].lower() == 'high'})
    return res

def get_items_list_for_country(df, country_code):
    '''
    The user has selected the country, we give the items available
     (ones that have valid links)

    '''
    country_codes = get_country_codes(df)
    if country_code not in country_codes:
        raise CountryCodeError('Country code not found: '+country_code)

    index = list(df.index)
    lang_codes = get_language_codes(df)
    item_names_by_language = []
    for i in range(len(df)):
        new_entry = {}
        for code in lang_codes:
            new_entry[code] = df['Name '+code].iloc[i]
        item_names_by_language.append(new_entry)

    item_priorities = list(df['Priority'])
    res = []
    for i in range(len(index)):
        links_raw = df['Links '+country_code].iloc[i]
        links_valid = split_and_filter_links(links_raw)
        if not links_valid: # no valid links found, don't include this row
            continue
        res.append({'row_number': index[i],
                    'item_names_by_language': item_names_by_language[i],
                    'is_high_priority': item_priorities[i].lower() == 'high'})
    return res

class MedicineReader():
    '''
    Reads the spreadsheet and returns dataframes with items.
    Place the client_secret.json file into the same directory; don't add the file to git!
    '''
    def __init__(self, PATH_TO_CREDS='client_secret.json',
                 SPREADSHEET_KEY='1qR7voq_HkeurKy-5m8gWjBVcuH1-HoW0x_bhAKbK8q8', using_cache=True):
        '''
        NB: Possible problem in the future - if the user waits too long,
        pygsheets might stop working and we'll have to authorize again.
        todo: test it and find a solution
        '''
        self.df_defence = None
        self.df_meds = None

        EXPIRATION_TIME = os.getenv('MEDICINE_REDIS_EXPIRATION') or 3600
        DEFENCE_KEY = 'MEDICINE-DEFENCE-DF'
        MEDS_KEY = 'MEDICINE-MEDS-DF'

        if using_cache:
            try:
                r = redis.StrictRedis(host=os.getenv('MEDICINE_REDIS_HOST') or 'localhost', port=os.getenv('MEDICINE_REDIS_PORT') or 6379, db=0)
                r.exists('test')  # Sanity check that always returns false!
            except redis.exceptions.ConnectionError:
                raise RedisConnectionError("Could not connect to the Redis host.")

            dfs_count = 0 # a flag to show we have all dataframes
            
            if r.exists(DEFENCE_KEY):
                self.df_defence = pickle.loads(zlib.decompress(r.get(DEFENCE_KEY)))
                dfs_count += 1
            
            if r.exists(MEDS_KEY):
                self.df_meds = pickle.loads(zlib.decompress(r.get(MEDS_KEY)))
                dfs_count += 1
            
            if dfs_count == 2:
                return

        # If we get here, we need to pull the data from Google.
        client = pygsheets.authorize(service_file=PATH_TO_CREDS)  # a file with the API credentials
        table = client.open_by_key(SPREADSHEET_KEY)
        worksheets = table.worksheets()
        sheets = {'meds': worksheets[0],
                  'defence': worksheets[1],
                  'info': worksheets[2],
                  'issues': worksheets[3],
                  'goals_reached': worksheets[4]}

        # First 4 rows in worksheeets 1-2 are for the info, not part of the actual table
        self.df_meds = sheets['meds'].get_as_df(start='A5')
        self.df_defence = sheets['defence'].get_as_df(start='A5')

        if using_cache:
            r.setex(MEDS_KEY, EXPIRATION_TIME, zlib.compress(pickle.dumps(self.df_meds)))
            r.setex(DEFENCE_KEY, EXPIRATION_TIME, zlib.compress(pickle.dumps(self.df_defence)))
        
        # todo: add the remaining 3 sheets? (they are currently too noisy to convert to df)
