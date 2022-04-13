from django.core import management
from django.core.management.base import BaseCommand

class Command(BaseCommand):
    """
    Executes calls for the CRON job on the Medicine for Ukraine server.
    """
    help = 'Flushes the cache and runs the link repopulation scripts.'

    def handle(self, *args, **options):
        management.call_command('flushcache')
        management.call_command('link_sheet_populator')
        management.call_command('link_database_populator')