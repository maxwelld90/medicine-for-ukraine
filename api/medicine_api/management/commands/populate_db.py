import os
from medicine_api import models
from django.db.utils import OperationalError
from django.core.management.base import BaseCommand, CommandError

class Command(BaseCommand):
    """
    A simple Django command to provide a simple dataset for the database (for testing purposes).
    """
    help = 'Populates the Medicine for Ukraine database with some sample data for testing'

    def __create_country(self):
        """
        Creates a sample Country object.
        """
        self.stdout.write(self.style.NOTICE("Creating Country object..."))
        language_dict = models.get_default_language_dict()
        language_dict['en'] = 'Poland'

        country = models.Country(
            code = 'pl',
            names = language_dict,
            flag_url = 'pl.svg'
        )

        country.save()
        return country
    
    def __create_warehouse(self, country):
        """
        Creates a Warehouse object.
        """
        self.stdout.write(self.style.NOTICE("Creating Warehouse object..."))
        
        warehouse = models.Warehouse(
            name = 'Warehouse in Poland',
            country = country,
            address = f'123 Fake Street{os.linesep}Some City{os.linesep}Poland{os.linesep}123456',
        )

        warehouse.save()
        return warehouse
    
    def __create_sheet(self):
        """
        Creates a Sheet object.
        """
        self.stdout.write(self.style.NOTICE("Creating Sheet object..."))

        sheet = models.Sheet(
            name = 'olena',
        )

        sheet_links = models.Sheet(
            name = 'links',
        )

        sheet.save()
        sheet_links.save()
        return sheet
    
    def __create_recipient(self, warehouse, sheet):
        """
        Creates a Recipient object.
        """
        self.stdout.write(self.style.NOTICE("Creating Recipient object..."))
        names_dict = models.get_default_language_dict()
        names_dict['en'] = 'Olena'

        tagline_dict = models.get_default_language_dict()
        tagline_dict['en'] = 'This is a tagline for Olena. She is looking to get medical equipment into Ukraine.'

        recipient = models.Recipient(
            names = names_dict,
            tagline = tagline_dict,
            warehouse = warehouse,
            sheet = sheet,
            email = 'mail@medicineforukraine.org',
            is_active = True,
        )

        recipient.save()
        return recipient

    def handle(self, *args, **options):
        try:
            country = self.__create_country()
            warehouse = self.__create_warehouse(country)
            sheet = self.__create_sheet()
            recipient = self.__create_recipient(warehouse, sheet)
        except OperationalError:
            raise CommandError(self.style.ERROR('The database doesn\'t have all the required tables. Did you run migrate?'))

        self.stdout.write(self.style.SUCCESS('Sample data successfully created.'))
        