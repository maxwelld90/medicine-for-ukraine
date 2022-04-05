from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from medicine_api.models import Country
from medicine_api.handlers.countries import serializers

class CountryListing(APIView):
    """
    Returns a listing of the countries that are in the database.
    """
    def get(self, request):
        try:
            countries = Country.objects.order_by('code')
            serializer = serializers.CountrySerializer(countries, many=True)
        except Exception as e:
            return Response({'message': str(e), 'exception': type(e).__name__}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        return_object = {
            'count': len(serializer.data),
            'countries': serializer.data
        }

        return Response(return_object, status=status.HTTP_200_OK)