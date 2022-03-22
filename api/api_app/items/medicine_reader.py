import os
import re
import redis
import pickle
import zlib
import warnings
import pygsheets
import pandas as pd
from copy import deepcopy
from django.conf import settings
from rest_framework import status


# Global module variables
REDIS_EXPIRATION_TIME = os.getenv('MEDICINE_REDIS_EXPIRATION') or 3600
REDIS_HOSTNAME = os.getenv('MEDICINE_REDIS_HOST') or 'localhost'
REDIS_PORT = os.getenv('MEDICINE_REDIS_PORT') or 6379
SHEET_KEY = '1qR7voq_HkeurKy-5m8gWjBVcuH1-HoW0x_bhAKbK8q8'  # The key for the Google Sheets document containing the data.
REDIS_SHEET_KEYS = {
    'defence': {
        'sheet': 'defence',
        'redis': 'MEDICINE-DEFENCE-DF'},
    'meds': {
        'sheet': 'meds',
        'redis': 'MEDICINE-MEDS-DF',
    }
}

# Custom exceptions for identifying issues within the medicine reader.
class UnknownDataframeError(Exception):
    pass

class GoogleConnectionError(Exception):
    pass

class CountryCodeError(Exception):
    pass

class RedisConnectionError(Exception):
    pass

class UnknownItemError(IndexError):
    pass

# Helper function that API views call to reduce repetition
def call_medicine_reader(data_name, method, params={}):
    return_object = {
        'data': {},
        'status': status.HTTP_200_OK,
    }
    
    try:
        reader = MedicineReader()
    except GoogleConnectionError:
        return_object['data']['message'] = 'There was a problem retrieving the data.'
        return_object['status'] = status.HTTP_500_INTERNAL_SERVER_ERROR
        return return_object
    except RedisConnectionError:
        return_object['data']['message'] = 'There was a problem with the caching the server.'
        return_object['status'] = status.HTTP_500_INTERNAL_SERVER_ERROR
        return return_object
    
    try:
        return_object['data'][data_name] = getattr(reader, method)(**params)
    except CountryCodeError:
        return_object['data']['message'] = f'The country code "{params["country_code"]}" was not recognised.'
        return_object['status'] = status.HTTP_404_NOT_FOUND
        return return_object
    except UnknownDataframeError:
        return_object['data']['message'] = f'The dataframe "{params["df_str"]}" was not recognised.'
        return_object['status'] = status.HTTP_404_NOT_FOUND
        return return_object
    except UnknownItemError:
        return_object['data']['message'] = f'The specified item with number {params["item_index"]} was not recognised.'
        return_object['status'] = status.HTTP_404_NOT_FOUND

    return return_object


# Helper Functions
url_validator = re.compile(
        r'^(?:http|ftp)s?://' # http:// or https://
        r'(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+(?:[A-Z]{2,6}\.?|[A-Z0-9-]{2,}\.?)|' #domain...
        r'localhost|' #localhost...
        r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})' # ...or ip
        r'(?::\d+)?' # optional port
        r'(?:/?|[/?]\S+)$', re.IGNORECASE)

def is_valid_url(url):
    return re.match(url_validator, url) is not None

def split_and_filter_links(links_text):
    """
    Takes the raw string from the links cell, and returns a nicely formatted list of (valid) URLs.
    """
    replacements = (',', '\n')

    for r in replacements:
        links_text = links_text.replace(r, ' ')
    
    res = links_text.split()
    return [link for link in res if is_valid_url(link)]

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

class MedicineReader(object):
    '''
    Reads the spreadsheet and returns dataframes with items.
    Place the client_secret.json file into the same directory; don't add the file to git!
    '''
    def __init__(self, using_cache=True):
        '''
        NB: Possible problem in the future - if the user waits too long,
        pygsheets might stop working and we'll have to authorize again.
        todo: test it and find a solution
        '''
        redis_conn = None
        self.__dataframes = {}

        if using_cache:
            redis_conn = self.connect_to_cache()
            
            if self.check_cache(redis_conn):
                return  # If we get here, the cache was populated and loaded.
        
        # If we get here, the cache was not being used, or was not populated (fully).
        self.get_sheets(using_cache, redis_conn)
        # todo: add the remaining 3 sheets? (they are currently too noisy to convert to df)
        
    def connect_to_cache(self):
        """
        Attempts to connect to the Redis cache, and returns the object if successful.
        Raises an exception if this fails.
        """
        try:
            redis_conn = redis.StrictRedis(host=REDIS_HOSTNAME,
                                  port=REDIS_PORT,
                                  db=0)
            redis_conn.exists('test')  # Forces the connection to establish; failures are captured from here.
        except redis.exceptions.ConnectionError:
            raise RedisConnectionError("Could not connect to the Redis host.")
        
        return redis_conn
    
    def check_cache(self, redis_conn):
        """
        Checks to see if the Redis cache has the necessary keys to use.
        Returns True if all keys are present; False otherwise.
        Sets the self.__dataframes instance variable.
        """
        present_dataframes = 0
        
        for df_sheet, df_values in REDIS_SHEET_KEYS.items():
            if redis_conn.exists(df_values['redis']):
                self.__dataframes[df_sheet] = pickle.loads(zlib.decompress(redis_conn.get(df_values['redis'])))
                present_dataframes += 1
        
        if len(REDIS_SHEET_KEYS.keys()) == present_dataframes:
            return True
        
        return False
    
    def get_sheets(self, use_cache, redis_conn=None):
        """
        Connects to the Google Sheets API to extract the necessary data.
        Populates the cache if required; sets the object's instance variables.
        """
        try:
            client = pygsheets.authorize(service_file=settings.GOOGLE_API_SECRET_PATH)
            table = client.open_by_key(SHEET_KEY)
            worksheets = table.worksheets()
        except Exception as e:
            raise GoogleConnectionError(f"An exception occurred connecting to the Google Sheets API. {str(e)}")
        
        # Correct as of 2022-03-07
        # Keys must match the keys in REDIS_SHEET_KEYS!
        sheets = {'meds': worksheets[0],
                  'defence': worksheets[1],
                  'info': worksheets[2],
                  'issues': worksheets[3],
                  'goals_reached': worksheets[4]}
        
        # First 4 rows in worksheeets 1-2 are for the info, not part of the actual table
        for df_sheet, df_values in REDIS_SHEET_KEYS.items():
            self.__dataframes[df_sheet] = sheets[df_values['sheet']].get_as_df(start='A5')

            if use_cache:
                redis_conn.setex(df_values['redis'],
                                 REDIS_EXPIRATION_TIME,
                                 zlib.compress(pickle.dumps(self.__dataframes[df_sheet])))
    
    def get_current_dataframes(self):
        return self.__dataframes.keys()
    
    def get_all_high_priority_items(self, df_str):
        if df_str not in self.__dataframes:
            raise UnknownDataframeError(f'The dataframe "{df_str}" is not recognised.')
        
        df = self.__dataframes[df_str]
        df_high = df[df['Priority'].apply(lambda s: s.lower()) == 'high']
        return self.__get_items_list(df_high)

    def get_items_list(self, df_str):
        """
        Given a dataframe string identifier (e.g., meds/defence), returns a list of items for that particular type.
        """
        if df_str not in self.__dataframes:
            raise UnknownDataframeError(f'The dataframe "{df_str}" is not recognised.')
        
        df = self.__dataframes[df_str]
        return self.__get_items_list(df)
    
    def __get_items_list(self, df):
        index = list(df.index)
        lang_codes = get_language_codes(df)
        item_names_by_language = []

        for i in range(len(df)):
            new_entry = {}
            
            for code in lang_codes:
                new_entry[code] = df[f'Name {code}'].iloc[i]
            
            item_names_by_language.append(new_entry)
        
        item_priorities = list(df['Priority'])
        res = []

        for i in range(len(index)):
            res.append({'row_number': index[i],
                        'item_names_by_language': item_names_by_language[i],
                        'is_high_priority': item_priorities[i].lower() == 'high'})
        
        return res

    def get_items_list_for_country(self, df_str, country_code):
        """
        Given a dataframe string identifier (e.g., meds/defence) and a country code (e.g., PL), returns a list of items available for that country with valid links.
        """
        if df_str not in self.__dataframes:
            raise UnknownDataframeError(f'The dataframe "{df_str}" is not recognised.')
        
        df = self.__dataframes[df_str]
        country_codes = get_country_codes(df)

        if country_code not in country_codes:
            raise CountryCodeError(f'Country code "{country_code}" not recognised.')
        
        index = list(df.index)
        lang_codes = get_language_codes(df)
        item_names_by_language = []

        for i in range(len(df)):
            new_entry = {}

            for code in lang_codes:
                new_entry[code] = df[f'Name {code}'].iloc[i]
            
            item_names_by_language.append(new_entry)
        
        item_priorities = list(df['Priority'])
        item_order_count = list(df['Ordered'])
        item_need_count = list(df['Need #'])
        res = []

        for i in range(len(index)):
            links_raw = df[f'Links {country_code}'].iloc[i]
            links_valid = split_and_filter_links(links_raw)

            if not links_valid:  # Skip this row; no valid links were found.
                continue
            
            res.append({'row_number': index[i],
                        'item_names_by_language': item_names_by_language[i],
                        'is_high_priority': item_priorities[i].lower() == 'high',
                        'number_ordered': item_order_count[i],
                        'number_needed': None if item_need_count[i] == '' else item_need_count[i],
                        })
        
        return res
    
    def get_links_for_item(self, df_str, country_code, item_index):
        '''
        df_str: a dataframe identifier for a table from our spreadsheet, already filtered by country!
        country_code: ES, PL, ..
        item_index: number of the row in df that contains our item

        returns a list of valid links for buying the item
        '''
        if df_str not in self.__dataframes:
            raise UnknownDataframeError(f'The dataframe "{df_str}" is not recognised.')
        
        df = self.__dataframes[df_str]
        country_codes = get_country_codes(df)

        if country_code not in country_codes:
            raise CountryCodeError(f'Country code "{country_code}" not recognised.')
        
        try:
            row = df.iloc[item_index]
        except IndexError:
            raise UnknownItemError(f'Item number {item_index} not found.')
        
        links_cell = row['Links {0}'.format(country_code)]
        links_list = split_and_filter_links(links_cell)

        if not links_list:
            warnings.warn('No valid URLs found for this item!')
        
        return links_list
    
    def get_language_codes(self, df_str):
        """
        df_str: a dataframe identifier for a table from our spreadsheet, already filtered by country!
        """
        if df_str not in self.__dataframes:
            raise UnknownDataframeError(f'The dataframe "{df_str}" is not recognised.')
        
        df = self.__dataframes[df_str]
        return get_language_codes(df)
        



# def select_country(df, country_code):
#     '''
#     df: a dataframe with a table (from our spreadsheet)
#     country_code: ES, PL, etc.
#     '''
#     # Filter out all columns for other countries except "Name EN"
#     columns_filtered = []
#     for column in df.columns:
#         if column != "Name EN" and column.startswith(('Name', 'Links')) and not column.endswith(country_code):
#             continue
#         columns_filtered.append(column)

#     df_res = deepcopy(df[columns_filtered])
#     return df_res

# def get_links_for_item(df, country_code, item_index):
#     '''
#     df: a dataframe with a table from our spreadsheet, already filtered by country!
#     country_code: ES, PL, ..
#     item_index: number of the row in df that contains our item

#     returns a list of valid links for buying the item
#     '''
#     country_codes = get_country_codes(df)
#     if country_code not in country_codes:
#         raise CountryCodeError(f'Country code not found: {country_code}')
    
#     try:
#         row = df.iloc[item_index]
#     except IndexError:
#         raise UnknownItemError(f'Item number {item_index} not found')

#     links_cell = row['Links {0}'.format(country_code)]
#     links_list = split_and_filter_links(links_cell)
#     if not links_list:
#         warnings.warn('No valid URLs found for this item!')
#     return links_list



# def get_items_list(df):
#     index = list(df.index)
#     lang_codes = get_language_codes(df)
#     item_names_by_language = []
#     for i in range(len(df)):
#         new_entry = {}
#         for code in lang_codes:
#             new_entry[code] = df['Name '+code].iloc[i]
#         item_names_by_language.append(new_entry)

#     item_priorities = list(df['Priority'])
#     res = []
#     for i in range(len(index)):
#         res.append({'row_number': index[i],
#                     'item_names_by_language': item_names_by_language[i],
#                     'is_high_priority': item_priorities[i].lower() == 'high'})
#     return res

# def get_items_list_for_country(df, country_code):
#     '''
#     The user has selected the country, we give the items available
#      (ones that have valid links)

#     '''
#     country_codes = get_country_codes(df)
#     if country_code not in country_codes:
#         raise CountryCodeError('Country code not found: '+country_code)

#     index = list(df.index)
#     lang_codes = get_language_codes(df)
#     item_names_by_language = []
#     for i in range(len(df)):
#         new_entry = {}
#         for code in lang_codes:
#             new_entry[code] = df['Name '+code].iloc[i]
#         item_names_by_language.append(new_entry)

#     item_priorities = list(df['Priority'])
#     res = []
#     for i in range(len(index)):
#         links_raw = df['Links '+country_code].iloc[i]
#         links_valid = split_and_filter_links(links_raw)
#         if not links_valid: # no valid links found, don't include this row
#             continue
#         res.append({'row_number': index[i],
#                     'item_names_by_language': item_names_by_language[i],
#                     'is_high_priority': item_priorities[i].lower() == 'high'})
#     return res

# class MedicineReader():
#     '''
#     Reads the spreadsheet and returns dataframes with items.
#     Place the client_secret.json file into the same directory; don't add the file to git!
#     '''
#     def __init__(self, using_cache=True):
#         '''
#         NB: Possible problem in the future - if the user waits too long,
#         pygsheets might stop working and we'll have to authorize again.
#         todo: test it and find a solution
#         '''
#         self.df_defence = None
#         self.df_meds = None

#         EXPIRATION_TIME = os.getenv('MEDICINE_REDIS_EXPIRATION') or 3600
#         DEFENCE_KEY = 'MEDICINE-DEFENCE-DF'
#         MEDS_KEY = 'MEDICINE-MEDS-DF'

#         if using_cache:
#             try:
#                 r = redis.StrictRedis(host=os.getenv('MEDICINE_REDIS_HOST') or 'localhost', port=os.getenv('MEDICINE_REDIS_PORT') or 6379, db=0)
#                 r.exists('test')  # Sanity check that always returns false!
#             except redis.exceptions.ConnectionError:
#                 raise RedisConnectionError("Could not connect to the Redis host.")

#             dfs_count = 0 # a flag to show we have all dataframes
            
#             if r.exists(DEFENCE_KEY):
#                 self.df_defence = pickle.loads(zlib.decompress(r.get(DEFENCE_KEY)))
#                 dfs_count += 1
            
#             if r.exists(MEDS_KEY):
#                 self.df_meds = pickle.loads(zlib.decompress(r.get(MEDS_KEY)))
#                 dfs_count += 1
            
#             if dfs_count == 2:
#                 return

#         # If we get here, we need to pull the data from Google.
#         client = pygsheets.authorize(service_file=settings.GOOGLE_API_SECRET_PATH)  # a file with the API credentials
#         table = client.open_by_key(SPREADSHEET_KEY)
#         worksheets = table.worksheets()
#         sheets = {'meds': worksheets[0],
#                   'defence': worksheets[1],
#                   'info': worksheets[2],
#                   'issues': worksheets[3],
#                   'goals_reached': worksheets[4]}

#         # First 4 rows in worksheeets 1-2 are for the info, not part of the actual table
#         self.df_meds = sheets['meds'].get_as_df(start='A5')
#         self.df_defence = sheets['defence'].get_as_df(start='A5')

#         if using_cache:
#             r.setex(MEDS_KEY, EXPIRATION_TIME, zlib.compress(pickle.dumps(self.df_meds)))
#             r.setex(DEFENCE_KEY, EXPIRATION_TIME, zlib.compress(pickle.dumps(self.df_defence)))
        
#         # todo: add the remaining 3 sheets? (they are currently too noisy to convert to df)

