from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from api_app.items import medicine_reader

class ItemsListForCountry(APIView):
    def get(self, request, equipment_type, country_code):
        equipment_type = equipment_type.lower()

        return_object = {
            'status': 'success',
            'equipment_type': equipment_type,
        }
        
        try:
            reader = medicine_reader.MedicineReader()
        except medicine_reader.RedisConnectionError:
            return_object['status'] = 'error'
            return_object['count'] = 0
            return_object['message'] = f'There was a problem with the caching the server.'
            return Response(return_object, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        dataframes = {
            'meds': reader.df_meds,
            'defence': reader.df_defence,
        }

        ## If a bad equipment type is supplied.
        if equipment_type not in dataframes.keys():
            return_object['status'] = 'error'
            return_object['count'] = 0
            return_object['message'] = f'The equipment type "{equipment_type}" was not found.'

            return Response(return_object, status=status.HTTP_404_NOT_FOUND)

        ## If this passes, this is a successful response.
        try:
            return_object['items'] = medicine_reader.get_items_list_for_country(dataframes[equipment_type], country_code)
            return_object['count'] = len(return_object['items'])
        
        ## If a bad country code is supplied.
        except medicine_reader.CountryCodeError:
            return_object['status'] = 'error'
            return_object['count'] = 0
            return_object['message'] = f'The country code "{country_code}" was not recognised.'
            return Response(return_object, status=status.HTTP_404_NOT_FOUND)

        return Response(return_object, status=status.HTTP_200_OK)

class LinksForItem(APIView):
    def get(self, request, equipment_type, country_code, item_index):
        equipment_type = equipment_type.lower()

        return_object = {
            'status': 'success',
            'equipment_type': equipment_type,
        }

        return_object = {
            'status': 'success',
            'equipment_type': equipment_type,
        }
        
        try:
            reader = medicine_reader.MedicineReader()
        except medicine_reader.RedisConnectionError:
            return_object['status'] = 'error'
            return_object['count'] = 0
            return_object['message'] = f'There was a problem with the caching the server.'
            return Response(return_object, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
        dataframes = {
            'meds': reader.df_meds,
            'defence': reader.df_defence,
        }

        ## If a bad equipment type is supplied.
        if equipment_type not in dataframes.keys():
            return_object['status'] = 'error'
            return_object['count'] = 0
            return_object['message'] = f'The equipment type "{equipment_type}" was not found.'

            return Response(return_object, status=status.HTTP_404_NOT_FOUND)
        
        try:
            return_object['link'] = medicine_reader.get_links_for_item(dataframes[equipment_type], country_code, item_index)
            return_object['count'] = len(return_object['link'])
        
        # If a bad item number has been defined.
        except medicine_reader.UnknownItemError:
            return_object['status'] = 'error'
            return_object['count'] = 0
            return_object['message'] = f'The item with number {item_index} was not found for country "{country_code}".'

            return Response(return_object, status=status.HTTP_404_NOT_FOUND)
        
        # If a bad country code has been supplied.
        except medicine_reader.CountryCodeError:
            return_object['status'] = 'error'
            return_object['count'] = 0
            return_object['message'] = f'The country with code "{country_code}" was not found.'

            return Response(return_object, status=status.HTTP_404_NOT_FOUND)
        
        if return_object['count'] == 0:
            return_object['status'] = 'success'
            return_object['count'] = 0
            return_object['message'] = f'There are no links for item {item_index} in country "{country_code}".'

            return Response(return_object, status=status.HTTP_204_NO_CONTENT)
        
        return Response(return_object, status=status.HTTP_200_OK)