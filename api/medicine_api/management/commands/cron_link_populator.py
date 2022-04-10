import os
import logging
from medicine_api import models
from medicine_api.readers.price_reader import PriceReader
from django.core.management.base import BaseCommand, CommandError

logger = logging.getLogger('medicine_api.readers.sheet_reader')

class Command(BaseCommand):
    """
    Runs the CRON job to (re)populate the LinkMetadata model with refreshed information from the spreadsheet source.
    """
    help = '(Re)populates the Medicine for Ukraine links with updated information'

    def handle(self, *args, **options):
        logger.info('LINK UPDATING STARTING')
        
        price_reader = PriceReader()
        df_prices = price_reader.get_prices()
        
        for row in df_prices.itertuples():
            #logger.info(row.link)
            metadata_object = models.LinkMetadata()
            metadata_object.set_from_named_tuple(row)

        #logger.info('LINK UPDATING COMPLETE')
        self.stdout.write(self.style.SUCCESS('Links successfully updated.'))
        