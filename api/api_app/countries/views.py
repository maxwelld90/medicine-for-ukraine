from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from api_app.models import Address, Country
from api_app.countries import serializers
from api_app.items.medicine_reader import call_medicine_reader

class CountryListing(APIView):
    def get(self, request):
        countries = Country.objects.all()
        serializer = serializers.CountrySerializer(countries, many=True)

        return Response(serializer.data, status=status.HTTP_200_OK)

class CountryAddress(APIView):
    def get(self, request, country_code):
        addresses = Address.objects.filter(country__code=country_code, is_active=True)
        serializer = serializers.AddressSerializer(addresses, many=True)
        
        return Response(serializer.data, status=status.HTTP_200_OK)

class LanguageCodeListing(APIView):
    def get(self, request):
        response = call_medicine_reader('language_codes', 'get_language_codes', {'df_str': 'meds'})
        return Response(response['data'], status=response['status'])