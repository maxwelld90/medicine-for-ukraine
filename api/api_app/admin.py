import tldextract
from api_app import models
from django.contrib import admin
from django.contrib.admin import AdminSite
from django.contrib.auth.models import User
from django.utils.html import format_html


class MedicineAdminSite(AdminSite):
    site_header = 'Medicine for Ukraine Administration'
    site_title = 'Medicine for Ukraine Administration'
    site_url = 'https://medicineforukraine.org/'
    index_title = 'The Medicine for Ukraine Administration Interface'


class AddressAdminDisplay(admin.ModelAdmin):
    list_display = ['address_listing', 'is_active']
    fields = (('country', 'is_active'), 'address_lines')

    def address_listing(self, obj):
        return f'{obj.id} - {obj.country}'
    
    address_listing.short_description = 'Address Record'


class CountryAdminDisplay(admin.ModelAdmin):
    list_display = ['country_listing']

    def country_listing(self, obj):
        return f'{obj.name} ({obj.code})'


class ItemPriceAdminDisplay(admin.ModelAdmin):
    list_display = ['spreadsheet_data', 'online_shop', 'price_formatted', 'last_checked']

    def spreadsheet_data(self, obj):
        return f'Sheet {obj.type}, row {obj.row_number}'
    
    def price_formatted(self, obj):
        return format_html(f'&euro;{obj.price}')
    
    def online_shop(self, obj):
        store_domain = tldextract.extract(obj.url)
        store_domain = f'{store_domain.domain}.{store_domain.suffix}'

        return format_html(f'<a href="{obj.url}" target="_blank">{store_domain}</a>')

    spreadsheet_data.short_description = "Spreadsheet Location"
    price_formatted.short_description = format_html("Price (&euro;)")
    online_shop.short_description = "Online Shop"


class UserRequestAdminDisplay(admin.ModelAdmin):
    list_display = ['created_datetime', 'email_used', 'target_country', 'shop_count', 'item_count']
    ordering = ('-date_time',)

    def email_used(self, obj):
        return f'{obj.email}'

    def created_datetime(self, obj):
        return f'{obj.date_time.strftime("%Y-%m-%d, %H:%M:%S")}'
    
    def target_country(self, obj):
        return f'{obj.country_to.name} ({obj.country_to.code})'
    
    def shop_count(self, obj):
        store_sessions = models.StoreSession.objects.filter(user_request=obj)
        return len(store_sessions)

    def item_count(self, obj):
        items = models.RequestedItem.objects.filter(store_session__user_request=obj)
        return len(items)
    
    def has_add_permission(self, request, obj=None):
        return False
    
    created_datetime.short_description = 'Date/Time (UTC)'
    email_used.short_description = 'E-Mail Address Used'
    target_country.short_description = 'Target Country'
    shop_count.short_description = 'Shop(s) Used'
    item_count.short_description = 'Unique Item(s) Requested'


class StoreSessionAdminDisplay(admin.ModelAdmin):
    list_display = ['online_shop', 'email', 'created_datetime']

    def online_shop(self, obj):
        store_domain = tldextract.extract(obj.store_domain)
        store_domain = f'{store_domain.domain}.{store_domain.suffix}'

        return f'{store_domain}'
    
    def email(self, obj):
        return obj.user_request.email
    
    def created_datetime(self, obj):
        return f'{obj.user_request.date_time.strftime("%Y-%m-%d, %H:%M:%S")}'
    
    def has_add_permission(self, request, obj=None):
        return False
    
    online_shop.short_description = 'Online Shop'
    email.short_description = 'E-Mail Address Used'
    created_datetime.short_description = 'Date/Time (UTC)'


class ScreenshotAdminDisplay(admin.ModelAdmin):
    list_display = ['online_shop', 'email', 'created_datetime', 'screenshot']

    def online_shop(self, obj):
        store_domain = tldextract.extract(obj.store_session.store_domain)
        store_domain = f'{store_domain.domain}.{store_domain.suffix}'

        return f'{store_domain}'

    def email(self, obj):
        return obj.store_session.user_request.email
    
    def created_datetime(self, obj):
        return f'{obj.store_session.user_request.date_time.strftime("%Y-%m-%d, %H:%M:%S")}'

    def screenshot(self, obj):
        return format_html(f'<a href="{obj.image.url}" target="_blank"><img src="{obj.image.url}" style="height: 100px;" alt="Thumbnail" /></a>')
    
    def has_add_permission(self, request, obj=None):
        return False
    
    online_shop.short_description = 'Online Shop'
    email.short_description = 'E-Mail Address Used'
    screenshot.short_description = 'Screenshot Thumbnail'
    created_datetime.short_description = 'Date/Time (UTC)'


class RequestedItemAdminDisplay(admin.ModelAdmin):
    list_display = ['name', 'online_shop', 'spreadsheet_data', 'quantity']

    def online_shop(self, obj):
        store_domain = tldextract.extract(obj.url)
        store_domain = f'{store_domain.domain}.{store_domain.suffix}'

        return format_html(f'<a href="{obj.url}" target="_blank">{store_domain}</a>')
    
    def spreadsheet_data(self, obj):
        return f'Sheet {obj.type}, row {obj.row_number}'
    
    def has_add_permission(self, request, obj=None):
        return False
    
    spreadsheet_data.short_description = 'Spreadsheet Location'
    online_shop.short_description = 'Online Shop'


admin_site = MedicineAdminSite(name='admin')

admin_site.register(models.Address, AddressAdminDisplay)
admin_site.register(models.Country, CountryAdminDisplay)
admin_site.register(models.ItemPrice, ItemPriceAdminDisplay)

admin_site.register(models.UserRequest, UserRequestAdminDisplay)
admin_site.register(models.StoreSession, StoreSessionAdminDisplay)
admin_site.register(models.Screenshot, ScreenshotAdminDisplay)
admin_site.register(models.RequestedItem, RequestedItemAdminDisplay)

admin_site.register(User)