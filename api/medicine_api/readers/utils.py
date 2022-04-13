import re
import statistics
from medicine_api.models import LinkMetadata


URL_VALIDATOR = re.compile(
        r'^(?:http|ftp)s?://' # http:// or https://
        r'(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+(?:[A-Z]{2,6}\.?|[A-Z0-9-]{2,}\.?)|' #domain...
        r'localhost|' #localhost...
        r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})' # ...or ip
        r'(?::\d+)?' # optional port
        r'(?:/?|[/?]\S+)$', re.IGNORECASE)

def is_valid_url(url):
    return re.match(URL_VALIDATOR, url) is not None

def split_and_filter_links(links_text):
    """
    Takes the raw string from the links cell, and returns a nicely formatted list of (valid) URLs.
    """
    replacements = (',', '\n')

    for r in replacements:
        links_text = links_text.replace(r, ' ')
    
    res = links_text.split()
    return [link for link in res if is_valid_url(link)]

def get_links_for_item(item_row):
    """
    Given a Series object, returns a list of all URLs/links for that specified item.
    This list of links is agnostic of any restrictions (e.g., out of stock, does not deliver to X, etc.).
    Returns an empty list if no links are present.
    """
    return_list = []

    for column_name in item_row.keys():
        if column_name.lower().startswith('links'):
            return_list.extend(split_and_filter_links(item_row[column_name]))
    
    return return_list

def filter_links(links_list, warehouse_country):
    """
    Performs link filtering. Filters by delivery country, and whether the link is in stock.
    Returns a list of tuples, with each tuple representing the URL and price for a link.
    Returns an empty list if no links remain.
    """
    return_list = []

    for link in links_list:
        try:
            link_metadata = LinkMetadata.objects.get(url=link)
        except LinkMetadata.DoesNotExist:
            # If the link was not found in the database, we purposefully ignore it for now.
            # Links that are not verified by a human should not be listed.
            continue
        
        if warehouse_country not in link_metadata.ships_to.all():
            # If the link does not ship to the country we are targeting (the warehouse location), we ignore it.
            continue
        
        if not link_metadata.in_stock:
            # If the link is not in stock, do not show it.
            continue
        
        return_list.append((link_metadata.url, link_metadata.price))
    
    return return_list

def get_mean_price_for_item(row, warehouse_country):
    """
    Assuming there is at least one item in the links list, returns the mean prices for those links.
    """
    links_list = filter_links(get_links_for_item(row), warehouse_country)
    prices = [item[1] for item in links_list]

    if len(prices) == 0:
        return 0.0
    
    return statistics.mean(prices)

def get_lowest_price_for_item(row, warehouse_country):
    """
    Assuming there is at least one item in the links list, returns the lowest price for those links.
    """
    links_list = filter_links(get_links_for_item(row), warehouse_country)
    prices = [item[1] for item in links_list]

    if len(prices) == 0:
        return 0.0
    
    return min(prices)

def process_name_strings(language_data, df):
    """
    Returns a dictionary of names for each of the different items specified in the DataFrame (df).
    The key denotes the row_number of each item. A nested dictionary is the value, with each language code as the key, and the value the name.
    If a language does not have a name/translation, None is provided in its place.
    The default language (typically EN) is specified as 'default'. This should be used as a fallback.
    """
    return_object = {}
    included_languages = []

    def map_to_dict(return_object, language_code, string_dict):
        """
        Nested function that takes data from the DataFrame and puts it into the return_object.
        """
        for row_number, name in string_dict.items():
            if row_number not in return_object.keys():
                return_object[row_number] = {}
            
            name = name.strip()

            if name == '':
                return_object[row_number][language_code] = None
            else:
                return_object[row_number][language_code] = name
    
    # Iterate over each of the columns, extracting the "name " fields.
    # Determines what languages we have available in the DataFrame.
    for column in df.columns:
        if column.startswith('name'):
            included_languages.append(column.lower().split()[-1])
    
    # Build up the dictionary to return.
    for language_code in language_data:
        try:
            string_name = df[f'name {language_code}']
            map_to_dict(return_object, language_code, string_name.to_dict())

            if language_data[language_code]['DEFAULT']:
                map_to_dict(return_object, 'default', string_name.to_dict())
        except KeyError:
            continue
    
    # Fill in the blanks - check each language we should be providing support for is mentioned.
    # If not, specify None in its place.
    for row_number in return_object.keys():
        for language_code in language_data:
            if language_code not in return_object[row_number].keys():
                return_object[row_number][language_code] = None
    
    return return_object