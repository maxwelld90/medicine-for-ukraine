from django.conf import settings
from rest_framework import serializers
from medicine_api.models import Recipient, Warehouse, ContactInformation
from medicine_api.handlers.countries.serializers import CountrySerializer

class RecipientSerializer(serializers.ModelSerializer):
    recipient_id = serializers.SerializerMethodField()
    names = serializers.SerializerMethodField()
    tagline = serializers.SerializerMethodField()
    requires_password = serializers.SerializerMethodField()
    contact_information = serializers.SerializerMethodField()
    warehouse_country = serializers.SerializerMethodField()

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
    
    def get_recipient_id(self, instance):
        return instance.id

    def get_names(self, instance):
        return_object = instance.names
        languages_data = settings.MEDICINE_LANGUAGE_DATA

        for language_code in languages_data.keys():
            if language_code not in return_object:
                return_object[language_code] = None
        
        return_object['default'] = instance.names[settings.LANGUAGE_CODE]
        return return_object
    
    def get_tagline(self, instance):
        return_object = instance.tagline
        languages_data = settings.MEDICINE_LANGUAGE_DATA

        for language_code in languages_data.keys():
            if language_code not in return_object:
                return_object[language_code] = None
        
        return_object['default'] = instance.tagline[settings.LANGUAGE_CODE]
        return return_object

    def get_requires_password(self, instance):
        return instance.password is not None
    
    def get_contact_information(self, instance):
        contact_information = ContactInformation.objects.filter(recipient=instance)
        serialized = ContactInformationSerializer(contact_information, many=True)

        return serialized.data
    
    def get_warehouse_country(self, instance):
        return CountrySerializer(instance.warehouse.country, many=False).data

    class Meta:
        model =  Recipient
        fields = ['recipient_id', 'names', 'tagline', 'requires_password', 'contact_information', 'warehouse_country']


class ContactInformationSerializer(serializers.ModelSerializer):
    string = serializers.SerializerMethodField()
    url = serializers.URLField()

    def get_string(self, instance):
        return_object = instance.string
        languages_data = settings.MEDICINE_LANGUAGE_DATA

        for language_code in languages_data.keys():
            if language_code not in return_object:
                return_object[language_code] = None
        
        return_object['default'] = instance.string[settings.LANGUAGE_CODE]
        return return_object

    class Meta:
        model = ContactInformation
        fields = ['string', 'url']


class WarehouseAddressSerializer(serializers.ModelSerializer):
    country = serializers.SerializerMethodField()
    address = serializers.CharField()

    def get_country(self, instance):
        return CountrySerializer(instance.country, many=False).data

    class Meta:
        model =  Warehouse
        fields = ['country', 'address']