from rest_framework.views import APIView
from rest_framework.response import Response
from api_app.models import ItemPrice
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
            else:
                updated = []

                for link in response['data']['links']:
                    item = {
                        'url': link,
                        'price': None,
                        'last_checked': None,
                    }

                    try:
                        price_point = ItemPrice.objects.get(url=link)
                        item['price'] = price_point.price
                        item['last_checked'] = price_point.last_checked
                    except ItemPrice.DoesNotExist:
                        pass

                    updated.append(item)
                
                response['data']['links'] = updated
        
        return Response(response['data'], status=response['status'])