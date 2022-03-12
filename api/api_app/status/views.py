from rest_framework.views import APIView
from rest_framework.response import Response
from api_app.models import Country
from api_app.items.medicine_reader import call_medicine_reader
from rest_framework import status


class ServerStatus(APIView):
    def get(self, request):
        countries = Country.objects.all()

        if len(countries) == 0:
            return Response({}, status=status.HTTP_204_NO_CONTENT)  # We can't do the checks as there's no data to pull out!
        
        response = call_medicine_reader('items',
                                        'get_items_list_for_country',
                                        {'df_str': 'meds', 'country_code': countries[0].code})
        
        if response['status'] != 200:
            return Response({}, status=status.HTTP_503_SERVICE_UNAVAILABLE)

        return Response({}, status=status.HTTP_200_OK)