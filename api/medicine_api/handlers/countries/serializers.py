from django.conf import settings
from rest_framework import serializers
from medicine_api.models import Country

class CountrySerializer(serializers.ModelSerializer):
    code = serializers.CharField(max_length=5)
    names = serializers.SerializerMethodField()
    flag_url = serializers.CharField(max_length=256)

    def get_names(self, instance):
        return_object = instance.names
        languages_data = settings.MEDICINE_LANGUAGE_DATA

        for language_code in languages_data.keys():
            if language_code not in return_object:
                return_object[language_code] = None
        
        return_object['default'] = instance.names[settings.LANGUAGE_CODE]
        
        return return_object

    class Meta:
        model = Country
        fields = ['code', 'names', 'flag_url']