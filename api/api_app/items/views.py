from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from api_app.items.medicine_reader import call_medicine_reader


class ItemsListForCountry(APIView):
    def get(self, request, df_str, country_code):
        df_str = df_str.lower()
        response = call_medicine_reader('items',
                                        'get_items_list_for_country',
                                        {'df_str': df_str, 'country_code': country_code})
        
        if response['status'] == 200:
            response['data']['df_str'] = df_str
            response['data']['count'] = len(response['data']['items'])

        return Response(response['data'], status=response['status'])


class LinksForItem(APIView):
    def get(self, request, df_str, country_code, item_index):
        df_str = df_str.lower()
        response = call_medicine_reader('links',
                                        'get_links_for_item',
                                        {'df_str': df_str, 'country_code': country_code, 'item_index': item_index})
        
        if response['status'] == 200:
            response['data']['df_str'] = df_str
            response['data']['country_code'] = country_code
            response['data']['count'] = len(response['data']['links'])

            if response['data']['count'] == 0:
                response['status'] = 204
        
        return Response(response['data'], status=response['status'])



        # equipment_type = equipment_type.lower()

        # return_object = {
        #     'status': 'success',
        #     'equipment_type': equipment_type,
        # }

        # return_object = {
        #     'status': 'success',
        #     'equipment_type': equipment_type,
        # }
        
        # try:
        #     reader = medicine_reader.MedicineReader()
        # except medicine_reader.RedisConnectionError:
        #     return_object['status'] = 'error'
        #     return_object['count'] = 0
        #     return_object['message'] = f'There was a problem with the caching the server.'
        #     return Response(return_object, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
        # dataframes = {
        #     'meds': reader.df_meds,
        #     'defence': reader.df_defence,
        # }

        # ## If a bad equipment type is supplied.
        # if equipment_type not in dataframes.keys():
        #     return_object['status'] = 'error'
        #     return_object['count'] = 0
        #     return_object['message'] = f'The equipment type "{equipment_type}" was not found.'

        #     return Response(return_object, status=status.HTTP_404_NOT_FOUND)
        
        # try:
        #     return_object['link'] = medicine_reader.get_links_for_item(dataframes[equipment_type], country_code, item_index)
        #     return_object['count'] = len(return_object['link'])
        
        # # If a bad item number has been defined.
        # except medicine_reader.UnknownItemError:
        #     return_object['status'] = 'error'
        #     return_object['count'] = 0
        #     return_object['message'] = f'The item with number {item_index} was not found for country "{country_code}".'

        #     return Response(return_object, status=status.HTTP_404_NOT_FOUND)
        
        # # If a bad country code has been supplied.
        # except medicine_reader.CountryCodeError:
        #     return_object['status'] = 'error'
        #     return_object['count'] = 0
        #     return_object['message'] = f'The country with code "{country_code}" was not found.'

        #     return Response(return_object, status=status.HTTP_404_NOT_FOUND)
        
        # if return_object['count'] == 0:
        #     return_object['status'] = 'success'
        #     return_object['count'] = 0
        #     return_object['message'] = f'There are no links for item {item_index} in country "{country_code}".'

        #     return Response(return_object, status=status.HTTP_204_NO_CONTENT)
        
        # return Response(return_object, status=status.HTTP_200_OK)