import os
import logging
from medicine_api import models
from medicine_api.readers.price_reader import PriceReader
from django.core.management.base import BaseCommand

logger = logging.getLogger('medicine_api.readers.link_database_populator')

class Command(BaseCommand):
    """
    Runs the CRON job to (re)populate the LinkMetadata model with refreshed information from the spreadsheet source.
    """
    help = '(Re)populates the Medicine for Ukraine links database table with updated information.'

    def handle(self, *args, **options):
        logger.info('Link Database Checks Starting')
        
        price_reader = PriceReader()
        data = price_reader.get_link_data()
        
        for item in data:
            metadata_object = models.LinkMetadata()
            metadata_object.set_from_link_data(item)

        logger.info('Link Database Checks Complete')
        self.stdout.write(self.style.SUCCESS('Link checking successfully completed.'))
        