import os
from medicine_api import models
from medicine_api.readers.price_reader import PriceReader
from django.core.management.base import BaseCommand, CommandError

class Command(BaseCommand):
    """
    Runs the CRON job to (re)populate the LinkMetadata model with refreshed information from the spreadsheet source.
    """
    help = '(Re)populates the Medicine for Ukraine links with updated information'

    def handle(self, *args, **options):
        price_reader = PriceReader(using_cache=True)
        df_prices = price_reader.get_prices()
        
        for row in df_prices.itertuples():
            self.stdout.write(self.style.NOTICE(f'Processing link {row.link}'))
            metadata_object = models.LinkMetadata()
            metadata_object.set_from_named_tuple(row)

        self.stdout.write(self.style.SUCCESS('Links successfully updated.'))
        