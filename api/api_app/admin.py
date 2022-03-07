from django.contrib import admin
from api_app import models

class CountryAdminDisplay(admin.ModelAdmin):
    list_display = ['name']

admin.site.register(models.Address)
admin.site.register(models.Country, CountryAdminDisplay)