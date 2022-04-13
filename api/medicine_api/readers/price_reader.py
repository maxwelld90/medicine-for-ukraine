from pytz import timezone
from datetime import datetime
from medicine_api.readers.sheet_reader import SheetReader


class PriceReader(SheetReader):
    def __init__(self):
        self._data_key = 'sheetReader'
        super().__init__()
    
    def __get_links_dataframe(self):
        """
        Returns the links DataFrame object.
        """
        return self._dataframes['links']
    
    def __generate_link_metaobject(self, row):
        row_dict = dict(row[1])

        def to_date(value):
            if value == '':
                return None
            
            amsterdam = timezone('Europe/Amsterdam')
            return datetime.strptime(value, '%Y-%m-%dT%H:%M:%S').replace(tzinfo=amsterdam)

        def to_bool(value):
            selection = {
                '': False,
                'FALSE': False,
                'TRUE': True,
            }

            if value not in selection.keys():
                return False
            
            return selection[value]
        
        def to_float(value):
            if type(value) == int:
                return float(value)
            
            value = value.replace(',', '.')

            try:
                value = float(value)
            except ValueError:
                return None

            return value
        
        del row_dict['comments']
        del row_dict['row_number']

        row_dict['date checked'] = to_date(row_dict['date checked'])
        row_dict['page available'] = to_bool(row_dict['page available'])
        row_dict['in stock'] = to_bool(row_dict['in stock'])
        row_dict['approx. price'] = to_float(row_dict['approx. price'])

        shipping_data = {k[9:]: to_bool(v) for k,v in row_dict.items() if k.startswith('ships to ')}

        for key in shipping_data.keys():
            del row_dict[f'ships to {key}']
        
        row_dict['last_checked'] = row_dict.pop('date checked')
        row_dict['price'] = row_dict.pop('approx. price')
        row_dict['in_stock'] = row_dict.pop('in stock')
        row_dict['available'] = row_dict.pop('page available')
        row_dict['url'] = row_dict.pop('link')
        row_dict['ships_to'] = shipping_data

        return row_dict
    
    def get_link_data(self):
        """
        Returns a list of dictionary objects. Each dictionary represents data for a URL from the DataFrame.
        """
        links_df = self.__get_links_dataframe()
        link_data = [self.__generate_link_metaobject(row) for row in links_df.iterrows()]

        return link_data

    def has_link(self, url):
        """
        Is the URL specified in the DataFrame?
        If the URL is specified, we have previously seen it, so return True. If not, we return False.
        """
        links_df = self.__get_links_dataframe()
        match = links_df.loc[links_df['link'] == url]

        if len(match) == 0:
            return False
        
        return True
    
