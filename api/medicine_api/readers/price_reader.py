from copy import deepcopy
from medicine_api.readers.sheet_reader import SheetReader

class PriceReader(SheetReader):
    """
    Extending the SheetReader, provides functionality for reading the URL price listings sheet.
    """

    def __init__(self, using_cache=True):
        super().__init__(using_cache=using_cache,
                         document_id='1vmqaQsLm5RAj1f_LT6rqpOfbkCSpvZiJ8PftF8KrJ_E',
                         required_sheets=[
                            'links_prices',
                         ])
    
    def get_prices(self):
        return_df = deepcopy(self._dataframes['links_prices'])

        # This will need to be refactored as more countries come online.
        return_df.rename(inplace=True,
                         columns={
                            'shipping to poland available?':'ships_to_poland', 
                            'approx. price (eur)':'approx_price_eur'},
                        )
        
        return return_df