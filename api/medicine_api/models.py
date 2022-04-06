from ast import Store
from unicodedata import name
import uuid
import pytz
from django.db import models
from datetime import datetime
from django.conf import settings
from django.core.exceptions import ValidationError


def validate_language_dict(value):
    default_language = settings.LANGUAGE_CODE

    if default_language not in value:
        raise ValidationError(f'Default language "{default_language}" is not specified.')
    
    if value[default_language] is None:
        raise ValidationError(f'Default language "{default_language}" is not specified.')

def get_default_language_dict():
    return {language_code: None for language_code in settings.MEDICINE_LANGUAGE_DATA.keys()}


class LowercaseCharField(models.CharField):
    """
    Solution from: https://stackoverflow.com/a/49181581
    Provides a CharField that guarantees the string representation is lowercased.
    """
    def __init__(self, *args, **kwargs):
        super(LowercaseCharField, self).__init__(*args, **kwargs)

    def get_prep_value(self, value):
        return str(value).lower()


class Country(models.Model):
    """
    Stores country information. Code is the PK (as a string, e.g., "PL").
    Codes must match the language codes that are returned from the spreadsheet!
    """
    code = LowercaseCharField(max_length=5,
                              primary_key=True,
                              help_text="The country code (e.g., pl for Poland). Codes are converted to lowercase automatically.")
    
    names = models.JSONField(default=get_default_language_dict,
                             validators=[validate_language_dict],  # Multilingual!
                             help_text="The name of the country, in each of the languages required.")
    
    flag_url = models.CharField(max_length=256,
                                unique=True,
                                help_text="What is the filename of the country's flag?")

    class Meta:
        verbose_name = 'Country'
        verbose_name_plural = 'Countries'
    
    def __str__(self):
        if settings.LANGUAGE_CODE in self.names:
            return self.names[settings.LANGUAGE_CODE]
        
        return self.code

class Warehouse(models.Model):
    """
    Represents a delivery point, within a Country. Associated with a Recipient.
    """
    id = models.UUIDField(primary_key=True,
                          default=uuid.uuid4,
                          help_text="The unique identifier for the warehouse.")
    
    name = models.CharField(max_length=300,
                            help_text="A name for the warehouse location to identify it.")
    
    country = models.ForeignKey(Country,
                                on_delete=models.CASCADE,
                                help_text="The country in which this warehouse is located.")
    
    address = models.TextField(help_text="The address for delivery to this warehouse.")

    class Meta:
        verbose_name = 'Warehouse'
        verbose_name_plural = 'Warehouses'
    
    def __str__(self):
        return f'Warehouse in {self.country}'


class Sheet(models.Model):
    """
    Represents a sheet in the Google Sheets datasource (i.e., where the information all comes from!).
    """
    name = LowercaseCharField(max_length=100, primary_key=True)

    class Meta:
        verbose_name = 'Sheet'
        verbose_name_plural = 'Sheets'

    def __str__(self):
        return self.name


class Recipient(models.Model):
    """
    Represents an individual/organisation that requests items.
    An individual's items ship to a specific Warehouse.
    If a password is set, this means the Recipent has a private address; ContactInformation is then required.
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4)

    warehouse = models.ForeignKey(Warehouse,
                                  on_delete=models.CASCADE,
                                  help_text="The warehouse address to ship items for this recipient to.")

    names = models.JSONField(default=get_default_language_dict,  # Multilingual!
                             validators=[validate_language_dict],
                             help_text="The name of the recipient, in different languages. At a minimum, specify EN.")
    
    tagline = models.JSONField(default=get_default_language_dict,  # Multilingual!
                               validators=[validate_language_dict],
                               help_text="The tagline, providing a short description to entice users to click the recipient's link. What items are being sought?")
    
    sheet = models.ForeignKey(Sheet,
                              on_delete=models.CASCADE,
                              help_text="The name (tab) of the sheet on the Google Sheets spreadsheet file to use.")

    password = models.CharField(null=True,  # Optional; if set, this means the address for the recipient should be password protected.
                                blank=True,
                                max_length=50,
                                help_text="If the recipient's warehouse address should not be publicly made available, specify a password here to unlock the address. This is NOT encrypted.")

    email = models.EmailField(null=True,
                              blank=True,
                              help_text="Specify the e-mail address to send alerts to when items are requested by users.")  # Used to contact the recipient.

    is_active = models.BooleanField(help_text="Is the recipient currently looking for items? This will hide the recipient from the list if not checked.")

    class Meta:
        verbose_name = 'Recipient'
        verbose_name_plural = 'Recipients'

    def __str__(self):
        if settings.LANGUAGE_CODE in self.names:
            return self.names[settings.LANGUAGE_CODE]
        
        return self.id


class ContactInformation(models.Model):
    """
    Represents contact information (i.e., Telegram links, mailto links) for accessing the password for a Recipient.
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    recipient = models.ForeignKey(Recipient, on_delete=models.CASCADE)
    string = models.JSONField()  # Multilingual!
    url = models.URLField()

    class Meta:
        verbose_name = 'Contact Information Link'
        verbose_name_plural = 'Contact Information Links'

    def __str__(self):
        if settings.LANGUAGE_CODE in self.string:
            return self.string[settings.LANGUAGE_CODE]
        
        return self.id


class LinkMetadata(models.Model):
    """
    Provides metadata (including approximate pricing in EUR) for items at given URLs.
    """
    url = models.URLField(primary_key=True)
    price = models.DecimalField(max_digits=6, decimal_places=2)
    last_checked = models.DateTimeField()
    ships_to = models.ManyToManyField(Country, related_name='ships_to', blank=True)
    in_stock = models.BooleanField()

    class Meta:
        verbose_name = 'Link Metadata'
        verbose_name_plural = 'Crawled Link Metadata'

    def set_from_named_tuple(self, named_tuple):
        """
        Given an instance of LinkMetadata, updates values internally from an instance from named_tuple.
        """
        self.url = named_tuple.link

        try:
            self.price = float(named_tuple.approx_price_eur)
        except ValueError:
            return False
        
        if named_tuple.date_checked == '':
            # We don't add items that have not been checked manually to the DB.
            return False
        
        self.last_checked = datetime.strptime(named_tuple.date_checked, '%Y-%m-%d').replace(tzinfo=pytz.UTC)
        
        self.in_stock = True

        # If the link is recorded as being out of stock, we do not show it to the user.
        if named_tuple.in_stock.lower() == 'n':
            self.in_stock = False

        # At the moment, we only care about shipping to Poland.
        # For the future, we may need to change this to add other countries.
        if named_tuple.ships_to_poland.lower() == 'yes':
            self.save()

            poland = Country.objects.get(code='pl')
            self.ships_to.add(poland)
            self.save()
            return True
        else:
            poland = Country.objects.get(code='pl')

            if poland in self.ships_to.all():
                self.ships_to.remove(poland)
                self.save()
        
        return True
    
    def save(self, *args, **kwargs):
        self.last_checked = datetime.now().replace(tzinfo=pytz.UTC)
        super().save(*args, **kwargs)
    
    def __str__(self):
        return self.url


class UserRequest(models.Model):
    """
    Represents the submission of a user's request/donation - associated with this is one or more StoreSession objects.
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    date_time = models.DateTimeField(auto_now_add=True)
    ip_address = models.GenericIPAddressField()
    user_agent = models.TextField()
    recipient = models.ForeignKey(Recipient, on_delete=models.CASCADE)
    is_approved = models.BooleanField(default=False,
                                      help_text="If the items have been approved, this should be checked to reflect that.")

    class Meta:
        verbose_name = 'Submitted Request/Donation'
        verbose_name_plural = 'Submitted Requests/Donations'
    
    def __str__(self):
        return f'User Request {self.id} (for {self.recipient})'


class StoreSession(models.Model):
    """
    Represents a given session for a particular store.
    Each session is associated with a UserRequest, and each StoreSession has one or more items associated with it.
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    user_request = models.ForeignKey(UserRequest, on_delete=models.CASCADE)
    store_domain = models.TextField()

    def __str__(self):
        return f'Store session for {self.store_domain}'


class Screenshot(models.Model):
    """
    Represents the screenshot(s) uploaded for a given StoreSession.
    As such, each Screenshot is linked to a given store, and a given UserRequest.
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    store_session = models.ForeignKey(StoreSession, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='screenshots/')

    class Meta:
        verbose_name = 'Screenshot'
        verbose_name_plural = 'Screenshots'
    
    def __str__(self):
        return f'Screenshot for {self.store_session.store_domain}'


class RequestedItem(models.Model):
    """
    Represents the details for an item that has been selected by a user.
    Links back to a StoreSession (to identify the user) and LinkData (to identify the URL).
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    store_session = models.ForeignKey(StoreSession, on_delete=models.CASCADE)
    url = models.ForeignKey(LinkMetadata, on_delete=models.CASCADE)
    name = models.TextField()
    quantity = models.IntegerField()
    row_number = models.IntegerField()
    price_at_purchase = models.DecimalField(max_digits=6, decimal_places=2)

    class Meta:
        verbose_name = 'Requested Item Record'
        verbose_name_plural = 'Requested Item Records'

    def __str__(self):
        return self.name