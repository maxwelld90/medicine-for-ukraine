from rest_framework import serializers
from api_app.models import Address, Country

class CountrySerializer(serializers.ModelSerializer):
    code = serializers.CharField(max_length=5)
    name = serializers.CharField(max_length=256)
    flag_url = serializers.CharField(max_length=256)

    class Meta:
        model = Country
        fields = ['code', 'name', 'flag_url']

class AddressSerializer(serializers.ModelSerializer):
    address_lines = serializers.CharField()

    class Meta:
        model = Address
        fields = ['id', 'address_lines']
