import os
import tldextract
from medicine_api import models as medicine_models
from django.db import models
from django.conf import settings
from django.contrib import admin
from django.contrib.admin import AdminSite
from django.contrib.auth.models import User
from django.utils.html import format_html
from django_json_widget.widgets import JSONEditorWidget


class MedicineAdminSite(AdminSite):
    site_header = 'Medicine for Ukraine Administration'
    site_title = 'Medicine for Ukraine Administration'
    site_url = 'https://medicineforukraine.org/'
    index_title = 'Medicine for Ukraine Administration Interface'


class CountryAdminDisplay(admin.ModelAdmin):
    list_display = ['country']
    fields = ['code', 'flag_url', 'names']

    formfield_overrides = {
        models.JSONField: {'widget': JSONEditorWidget},
    }

    def has_delete_permission(self, request, obj=None):
        return False

    def get_readonly_fields(self, request, obj=None):
        if obj:  # If obj exists, this means we must be editing something that is already there.
            return ['code']
        else:  # If obj does not exist, it must be a new addition.
            return []

    def country(self, obj):
        return f'{obj} ({obj.code.upper()})'


class WarehouseAdminDisplay(admin.ModelAdmin):
    list_display = ['name', 'address_line', 'country']
    readonly_fields = ['id']

    def country(self, obj):
        if settings.LANGUAGES_CODE in obj.country.name:
            return obj.country.name[settings.LANGUAGES_CODE]
        
        return 'Country without a default name'
    
    def address_line(self, obj):
        return obj.address.split(os.linesep)[0]

    def has_delete_permission(self, request, obj=None):
        return False


class SheetAdminDisplay(admin.ModelAdmin):

    def has_delete_permission(self, request, obj=None):
        return False


class RecipientAdminDisplay(admin.ModelAdmin):
    list_display = ['recipient_name', 'warehouse_location', 'email', 'is_active', 'password_protected']
    fields = ['names', 'tagline', 'id', 'sheet', 'warehouse', 'password', 'email', 'is_active']
    readonly_fields = ['id', 'sheet', 'warehouse']

    formfield_overrides = {
        models.JSONField: {'widget': JSONEditorWidget},
    }

    def has_delete_permission(self, request, obj=None):
        return False

    def recipient_name(self, obj):
        if settings.LANGUAGE_CODE in obj.names.keys():
            return str(obj.names[settings.LANGUAGE_CODE])
        
        return 'Recipient with unknown name'
    
    def warehouse_location(self, obj):
        return obj.warehouse.country
    
    def password_protected(self, obj):
        return True if obj.password is not None else False
    
    password_protected.boolean = True


class ContactInformationAdminDisplay(admin.ModelAdmin):
    list_display = ['contact_link', 'url_link', 'recipient']
    fields = ['recipient', 'url', 'string']
    ordering = ['recipient']

    formfield_overrides = {
        models.JSONField: {'widget': JSONEditorWidget},
    }

    def contact_link(self, obj):
        return f'{obj}'
    
    def url_link(self, obj):
        return format_html(f'<a href="{obj.url}" target="_blank">{obj.url}</a>')


class LinkMetadataAdminDisplay(admin.ModelAdmin):
    list_display = ['domain', 'approx_price', 'last_check', 'in_stock', 'shipping_to']
    ordering = ['last_checked', 'in_stock']
    readonly_fields = ['url']

    def has_add_permission(self, request, obj=None):
        return False
    
    def has_delete_permission(self, request, obj=None):
        return False

    def domain(self, obj):
        domain_info = tldextract.extract(obj.url)
        return f'{domain_info.domain}.{domain_info.suffix}'
    
    def last_check(self, obj):
        return obj.last_checked.strftime("%B %d %Y")
    
    def approx_price(self, obj):
        return format_html(f'&euro;{obj.price}')
    
    def shipping_to(self, obj):
        return ','.join(country.code.upper() for country in obj.ships_to.all())


class UserRequestAdminDisplay(admin.ModelAdmin):
    list_display = ['id', 'ip_address', 'placed_at', 'recipient', 'is_approved']
    readonly_fields = ['id', 'ip_address', 'placed_at', 'user_agent', 'recipient']

    def placed_at(self, obj):
        return obj.date_time.strftime('%Y-%m-%d %H:%m UTC')
    
    def has_add_permission(self, request, obj=None):
        return False

    def has_delete_permission(self, request, obj=None):
        return False


class StoreSessionAdminDisplay(admin.ModelAdmin):
    list_display = ['id', 'store_domain', 'recipient', 'is_approved']
    readonly_fields = ['id', 'user_request', 'store_domain']

    def recipient(self, obj):
        return obj.user_request.recipient
    
    def is_approved(self, obj):
        return obj.user_request.is_approved
    
    is_approved.boolean = True

    def has_add_permission(self, request, obj=None):
        return False

    def has_delete_permission(self, request, obj=None):
        return False


class ScreenshotAdminDisplay(admin.ModelAdmin):
    list_display = ['store_domain', 'created_datetime', 'screenshot']
    readonly_fields = ['id', 'store_session', 'created_datetime', 'image']

    def store_domain(self, obj):
        store_domain = tldextract.extract(obj.store_session.store_domain)
        
        if store_domain.domain == '':
            store_domain = store_domain.suffix
        else:
            store_domain = f'{store_domain.domain}.{store_domain.suffix}'

        return f'{store_domain}'
    
    def created_datetime(self, obj):
        return f'{obj.store_session.user_request.date_time.strftime("%Y-%m-%d, %H:%M:%S")}'

    def screenshot(self, obj):
        return format_html(f'<a href="{obj.image.url}" target="_blank"><img src="{obj.image.url}" style="height: 100px;" alt="Thumbnail" /></a>')
    
    def has_add_permission(self, request, obj=None):
        return False
    
    def has_delete_permission(self, request, obj=None):
        return False
    
    store_domain.short_description = 'Store\'s Web Domain'
    screenshot.short_description = 'Screenshot Thumbnail'
    created_datetime.short_description = 'Date/Time (UTC)'


class RequestedItemAdminDisplay(admin.ModelAdmin):
    list_display = ['item_name', 'store_domain', 'quantity', 'price_at_purchase_time', 'recipient', 'is_approved']
    readonly_fields = ['id', 'store_session', 'url', 'name', 'quantity', 'row_number', 'price_at_purchase']

    def item_name(self, obj):
        return obj.name

    def store_domain(self, obj):
        store_domain = tldextract.extract(obj.store_session.store_domain)

        if store_domain.domain == '':
            store_domain = store_domain.suffix
        else:
            store_domain = f'{store_domain.domain}.{store_domain.suffix}'

        return f'{store_domain}'

    def price_at_purchase_time(self, obj):
        return format_html(f'&euro;{obj.price_at_purchase}')
    
    def recipient(self, obj):
        return obj.store_session.user_request.recipient
    
    def is_approved(self, obj):
        return obj.store_session.user_request.is_approved
    
    is_approved.boolean = True
    
    def has_add_permission(self, request, obj=None):
        return False

    def has_delete_permission(self, request, obj=None):
        return False
    
    item_name.short_description = 'Item Name'
    store_domain.short_description = 'Store\'s Web Domain'


admin_site = MedicineAdminSite(name='admin')

admin_site.register(medicine_models.Country, CountryAdminDisplay)
admin_site.register(medicine_models.ContactInformation, ContactInformationAdminDisplay)
admin_site.register(medicine_models.Recipient, RecipientAdminDisplay)
admin_site.register(medicine_models.LinkMetadata, LinkMetadataAdminDisplay)
admin_site.register(medicine_models.UserRequest, UserRequestAdminDisplay)
#admin_site.register(medicine_models.StoreSession, StoreSessionAdminDisplay)
admin_site.register(medicine_models.Screenshot, ScreenshotAdminDisplay)
admin_site.register(medicine_models.Sheet, SheetAdminDisplay)
admin_site.register(medicine_models.Warehouse, WarehouseAdminDisplay)
admin_site.register(medicine_models.RequestedItem, RequestedItemAdminDisplay)

admin_site.register(User)