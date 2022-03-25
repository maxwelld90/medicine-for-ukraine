from rest_framework.views import APIView
from rest_framework.response import Response
from api_app.models import ItemPrice, Country
from api_app.countries.serializers import CountrySerializer
from api_app.items.medicine_reader import call_medicine_reader
import random

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


class HighPriorityItems(APIView):
    def get(self, request, selection, df_str):
        """
        Selection can be 'all' (returns ALL high priority items), 'first' (returns the first item), or 'random' (random!)
        """
        df_str = df_str.lower()
        selection = selection.lower()
        response = call_medicine_reader('items',
                                        'get_all_high_priority_items',
                                        {'df_str': df_str})

        if selection not in ['first', 'random']:
            selection = 'all'
            
        if selection == 'first':
            response['data']['items'] = [response['data']['items'][0]]
        if selection == 'random':
            response['data']['items'] = random.sample(response['data']['items'], k=1)
        
        if response['status'] == 200:
            response['data']['df_str'] = df_str
            response['data']['count'] = len(response['data']['items'])
        
        response['data']['selection'] = selection

        return Response(response['data'], status=response['status'])


class LinksForItem(APIView):
    def get(self, request, df_str, country_code, item_index):
        df_str = df_str.lower()
        response = call_medicine_reader('links',
                                        'get_links_for_item',
                                        {'df_str': df_str, 'country_code': country_code, 'item_index': item_index})
        
        if response['status'] == 200:
            response['data']['df_str'] = df_str
            response['data']['country'] = CountrySerializer(Country.objects.get(code=country_code)).data
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