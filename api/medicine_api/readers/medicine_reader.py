import json
import tldextract
from math import isnan
from copy import deepcopy
from decimal import Decimal
from medicine_api.models import LinkMetadata
from medicine_api.readers import utils
from medicine_api.readers import exceptions
from medicine_api.readers.sheet_reader import SheetReader
from medicine_api.handlers.countries.serializers import CountrySerializer

RANKING_PROPORTIONAL_CONSTANT = 1.0
RANKING_MANY_RATIO = 0

RANKING_WEIGHT_PRIORITY = 1
RANKING_WEIGHT_NEED = 0.5
RANKING_WEIGHT_PRICE = 0.9


class MedicineReader(SheetReader):
    """
    Extending the SheetReader, provides functionality for reading the main items listings.
    """
    def __init__(self, using_cache=True):
        super().__init__(using_cache=using_cache,
                         document_id='1qR7voq_HkeurKy-5m8gWjBVcuH1-HoW0x_bhAKbK8q8',
                         required_sheets=[
                            'olena',
                            'meds',
                         ])
    
    def __recipient_check(func):
        """
        Decorator method to check that the requested DataFrame is loaded.
        """
        def inner(self, recipient):
            df_name = recipient.sheet.name

            if df_name not in self._dataframes.keys():
                raise exceptions.UnknownDataFrameError(df_name)
            
            return func(self, recipient)
        
        return inner
    
    @classmethod
    def __score_row(cls, row):
        """
        Given an item row (Series), returns a float representing the item's score.
        This score is determined by several different features.
        """
        # Priority
        priority_value = 1 if row.priority.lower() == 'high' else 0
        
        # Need Ratio
        ordered_value = 0 if row.ordered is None or type(row.ordered) == str or isnan(row.ordered) else row.ordered
        need_value = row['required']

        if type(row['required']) == str:
            if row['required'].lower() == 'many':
                need_ratio = 0  # If we need many items, set the ratio to low so it is promoted up.
        else:
            need_value = row['required']

            if ordered_value > need_value:
                need_ratio = Decimal(1)
            else:
                need_ratio = Decimal(ordered_value / need_value)

        # Price
        price_value = row.average_price

        # Sum the components together to yield a score
        priority_final = Decimal(RANKING_WEIGHT_PRIORITY) * priority_value
        need_final = Decimal(RANKING_WEIGHT_NEED) * (Decimal(1) - need_ratio)
        price_final = Decimal(RANKING_WEIGHT_PRICE) * (Decimal(RANKING_PROPORTIONAL_CONSTANT) / price_value)
        
        return priority_final + need_final + price_final
    
    @__recipient_check
    def get_items_for_recipient(self, recipient):
        """
        Given a Recipient object, returns a list of the items available from that recipient's Google sheet.
        Performs link filtering, item ranking (based on __score_row()) and data cleaning.
        """
        df_name = recipient.sheet.name
        warehouse_country = recipient.warehouse.country

        df = self._dataframes[df_name]
        df_copy = deepcopy(df)  # We manipulate this copy of the DataFrame instead...

        # Tidy up - do we need to rename columns to match the expected names?
        if 'keys' in self._required_dataframes[df_name]:
            for column_type, look_for in self._required_dataframes[df_name]['keys'].items():
                df_copy.rename(columns={look_for.lower(): column_type.lower()}, inplace=True)
        
        df_copy['required'] = df_copy.apply(
                    lambda row: None if row.required is None else row.required,
                    axis=1
                )
        
        df_copy['ordered'] = df_copy.apply(
                    lambda row: None if row.ordered == '' else row.ordered,
                    axis=1
                )

        # Perform item filtering - drop items for which no acceptable links exist.
        df_copy.drop(df_copy[df_copy.apply(
            lambda row: not utils.filter_links(utils.get_links_for_item(row), warehouse_country),
            axis=1
        )].index, inplace=True)

        # Compute the average price over all the acceptable links.
        df_copy['average_price'] = df_copy.apply(
            lambda row: utils.get_mean_price_for_item(row, warehouse_country),
            axis=1
        )

        df_copy['lowest_price'] = df_copy.apply(
            lambda row: '{:.2f}'.format(utils.get_lowest_price_for_item(row, warehouse_country)),
            axis=1
        )

        # For remaining links, apply ranking scores.
        # Adds a 'score' column.
        df_copy['score'] = df_copy.apply(
            lambda row: MedicineReader.__score_row(row),
            axis=1)
        df_copy.sort_values('score', ascending=False, inplace=True)

        # Final tidying up
        df_copy.drop('average_price', axis=1, inplace=True)

        df_copy['is_high_priority'] = df_copy.apply(
            lambda row: row.priority.lower() == 'high',
            axis=1
        )

        # Create the return JSON object.
        return_object = json.loads(df_copy.to_json(orient='records'))

        # Append the item names in their proper data structure.
        item_names = utils.process_name_strings(self._language_data, df_copy)

        # Append the item names to each item.
        for row in return_object:
            row['item_name_by_language'] = item_names[row['row_number']]

            # Remove any name or links columns.
            for column_name in list(row.keys()):
                if column_name.startswith('name ') or column_name.startswith('links '):
                    del row[column_name]
                
                if column_name == 'required' and row[column_name] == 'many':
                    row[column_name] = True
                
                # For any extra rows that we wish to drop, do so here.
                if 'drop_rows' in self._required_dataframes[df_name] and column_name in [x.lower() for x in self._required_dataframes[df_name]['drop_rows']]:
                    del row[column_name]

        return return_object
    
    def get_links_for_item(self, recipient, row_number):
        """
        Given a row number (item identifier) and recipient, returns a series of links and metadata for the given item.
        """
        df_name = recipient.sheet.name
        warehouse_country = recipient.warehouse.country
        
        df = self._dataframes[df_name]
        df_copy = deepcopy(df)

        # Perform item filtering - drop items for which no acceptable links exist.
        df_copy.drop(df_copy[df_copy.apply(
            lambda row: not utils.filter_links(utils.get_links_for_item(row), warehouse_country),
            axis=1
        )].index, inplace=True)

        filtered = df_copy.loc[df_copy['row_number'] == row_number]

        if filtered.shape[0] == 0:
            # The row with row_number was not found in the DataFrame.
            return []
        
        return_list = []

        for link in utils.filter_links(utils.get_links_for_item(filtered.iloc[0]), warehouse_country):
            link_object = {}
            link_metadata = LinkMetadata.objects.get(url=link[0])
            domain_info = tldextract.extract(link_metadata.url)
            
            link_object['url'] = link_metadata.url
            link_object['domain'] = f'{domain_info.domain}.{domain_info.suffix}'
            link_object['price'] = '{:.2f}'.format(link_metadata.price)
            link_object['last_checked'] = link_metadata.last_checked
            link_object['in_stock'] = link_metadata.in_stock
            link_object['ships_to'] = CountrySerializer(link_metadata.ships_to.all(), many=True).data
        
            return_list.append(link_object)

        return return_list