from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from api_app.models import Address, Country
from api_app.countries import serializers

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