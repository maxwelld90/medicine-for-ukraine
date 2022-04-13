import logging
from medicine_api import models
from medicine_api.readers.price_reader import PriceReader
from medicine_api.readers.medicine_reader import MedicineReader
from django.core import management
from django.core.management.base import BaseCommand

logger = logging.getLogger('medicine_api.readers.link_sheet_populator')

class Command(BaseCommand):
    """
    Extracts URLs from all active sheets on the Medicine for Ukraine Google Sheets, and populates the Links sheet.
    """
    help = 'Extracts URLs from the Google Sheets document, and populates the links sheet.'

    def handle(self, *args, **options):
        logger.info('Link Sheet Populator Staring')

        management.call_command('flushcache')

        medicine_reader = MedicineReader()
        price_reader = PriceReader()

        recipients = models.Recipient.objects.filter(is_active=True)
        new_count = 0

        for recipient in recipients:
            recipient_links = medicine_reader.get_all_links_for_recipient(recipient)

            # Compute a list of URLs that are not present in the links DataFrame.
            # These have not been seen before; we need to add them.
            links_to_add = [link for link in recipient_links if not price_reader.has_link(link)]  # Links that have not been placed into the links sheet

            if len(links_to_add) == 0:
                continue

            for link in links_to_add:
                logger.info(f'From "{recipient}": adding link "{link}"')
                price_reader.save_to_worksheet('links', {'Link': link})
                new_count +=1
        
        self.stdout.write(self.style.SUCCESS(f'Link Sheet Populator Complete. Added {new_count} new link(s).'))
        logger.info(f'Link Sheet Populator Complete. Added {new_count} new link(s).')