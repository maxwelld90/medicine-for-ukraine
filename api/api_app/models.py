from ast import Store
import uuid
from django.db import models


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
    code = LowercaseCharField(max_length=5, primary_key=True)
    name = models.CharField(max_length=256, unique=True)
    flag_url = models.CharField(max_length=256, unique=True)

    class Meta:
        verbose_name = 'Country'
        verbose_name_plural = 'Countries'
    
    def __str__(self):
        return self.name


class Address(models.Model):
    """
    Stores addresses. One-to-many relationship between Country.
    One country can have many addresses.
    Use is_active to disable an address without deleting it.
    """
    country = models.ForeignKey(Country, on_delete=models.CASCADE)
    address_lines = models.TextField()
    is_active = models.BooleanField()

    class Meta:
        verbose_name = 'Address'
        verbose_name_plural = 'Addresses'
    
    def __str__(self):
        return f'Address in {self.country.name}'


class ItemPrice(models.Model):
    """
    (Approximate) pricing (in EUR) for items.
    Used to provide an idea of how much something costs to users without them having to click links.
    """
    url = models.URLField(primary_key=True)
    price = models.DecimalField(max_digits=6, decimal_places=2)
    last_checked = models.DateTimeField()
    row_number = models.IntegerField()  # This is the row number from the spreadsheet for the item in question.
    type = models.TextField()  # What sheet does the item come from? (i.e., meds/defence).

    class Meta:
        verbose_name = 'Item Pricing Record'
        verbose_name_plural = 'Item Pricing Records'

    def __str__(self):
        return f'{self.url}'


class UserRequest(models.Model):
    """
    Request from a user. Stores the basic details associated with the request.
    Other models link back to this request.
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    date_time = models.DateTimeField(auto_now_add=True)
    ip_address = models.GenericIPAddressField()
    user_agent = models.TextField()
    email = models.EmailField()
    country_to = models.ForeignKey(Country, on_delete=models.CASCADE)
    address_to = models.ForeignKey(Address, on_delete=models.CASCADE)

    class Meta:
        verbose_name = 'User Request Record'
        verbose_name_plural = 'User Request Records'

    def __str__(self):
        return f'User request from {self.email}'


class StoreSession(models.Model):
    """
    Represents a given session for a particular store.
    Each session is associated with a user request, and each store session has one or more items associated with it.
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    user_request = models.ForeignKey(UserRequest, on_delete=models.CASCADE)
    store_domain = models.TextField()

    class Meta:
        verbose_name = 'Store Session Record'
        verbose_name_plural = 'Store Session Records'

    def __str__(self):
        return f'{self.store_domain} ({self.user_request.email})'


class Screenshot(models.Model):
    """
    Represents the screenshot taken for a given store session.
    As such, each screenshot is linked to a given store, and a given request.
    More than one screenshot per store session is possible.
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    store_session = models.ForeignKey(StoreSession, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='screenshots/')

    class Meta:
        verbose_name = 'Store Basket Screenshot Record'
        verbose_name_plural = 'Store Basket Screenshot Records'

    def __str__(self):
        return f'Screenshot for {self.store_session.user_request.email} ({self.store_session.store_domain})'


class RequestedItem(models.Model):
    """
    Represents the details for an item requested.
    Links back to a store session, which in turn can be used to obtain request information.
    """
    store_session = models.ForeignKey(StoreSession, on_delete=models.CASCADE)
    url = models.URLField()
    name = models.TextField()
    type = models.TextField()
    quantity = models.IntegerField()
    row_number = models.IntegerField()  # This is the row number from the spreadsheet for the item in question.

    class Meta:
        verbose_name = 'Requested Item'
        verbose_name_plural = 'Requested Items'
    
    def __str__(self):
        return f"{self.name} at {self.url}"