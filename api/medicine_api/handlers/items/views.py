from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from medicine_api.models import Recipient
from medicine_api.readers.medicine_reader import MedicineReader

class ItemsForRecipient(APIView):
    def get(self, request, recipient_id):
        try:
            recipient = Recipient.objects.get(id=recipient_id, is_active=True)
        except Recipient.DoesNotExist:
            return Response({'message': 'The specificed recipient does not exist.', 'exception': 'DoesNotExist'}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({'message': str(e), 'exception': type(e).__name__}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
        try:
            reader = MedicineReader()
            items = reader.get_items_for_recipient(recipient)
        except Exception as e:
            return Response({'message': str(e), 'exception': type(e).__name__}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        return_object = {}
        return_object['items'] = items
        return_object['recipient_id'] = recipient.id
        return_object['count'] = len(items)

        return Response(return_object, status=status.HTTP_200_OK)


class LinksForRecipientItem(APIView):
    def get(self, request, recipient_id, row_number):
        try:
            recipient = Recipient.objects.get(id=recipient_id, is_active=True)
        except Recipient.DoesNotExist:
            return Response({'message': 'The specificed recipient does not exist.', 'exception': 'DoesNotExist'}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({'message': str(e), 'exception': type(e).__name__}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
        try:
            reader = MedicineReader()
            links = reader.get_links_for_item(recipient, row_number)
        except Exception as e:
            return Response({'message': str(e), 'exception': type(e).__name__}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        return_object = {}
        return_object['links'] = links
        return_object['recipient_id'] = recipient.id
        return_object['row_number'] = row_number
        return_object['count'] = len(links)

        return Response(return_object, status=status.HTTP_200_OK)