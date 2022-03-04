from rest_framework import serializers
from api_app.models import Country

class CountrySerializer(serializers.ModelSerializer):
    name = serializers.CharField(max_length=256)
    flag_url = serializers.CharField(max_length=256)

    class Meta:
        model = Country
        fields = ['name', 'flag_url']