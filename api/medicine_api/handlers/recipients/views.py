from rest_framework import status
from rest_framework.views import APIView
from medicine_api.models import Recipient
from rest_framework.response import Response
from medicine_api.handlers.recipients import serializers


class RecipientListing(APIView):
    """
    Returns active recipients that are able to accept donations.
    """
    def get(self, request):
        try:
            recipients = Recipient.objects.filter(is_active=True)
            serializer = serializers.RecipientSerializer(recipients, many=True)

            return_object = {
                'count': len(serializer.data),
                'recipients': serializer.data
            }
        except Exception as e:
            return Response({'message': str(e), 'exception': type(e).__name__}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        return Response(return_object, status=status.HTTP_200_OK)


class WarehouseAddress(APIView):
    """
    Given a recipient ID, returns details on the address for the recipient's warehouse.
    If a password is required, the password must be supplied as a querystring (?password=).
    """
    def get(self, request, recipient_id):
        try:
            recipient = Recipient.objects.get(id=recipient_id, is_active=True)
        except Recipient.DoesNotExist:
            return Response({'message': 'The specificed recipient does not exist.', 'exception': 'DoesNotExist'}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({'message': str(e), 'exception': type(e).__name__}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
        if recipient.password is not None:
            if 'password' in request.GET:
                password = request.GET.get('password')
                
                if password != recipient.password:
                    return Response({'message': 'You do not have the rights to access this address.', 'exception': 'Unauthorized'}, status=status.HTTP_403_FORBIDDEN)
            else:
                return Response({'message': 'You do not have the rights to access this address.', 'exception': 'Unauthorized'}, status=status.HTTP_403_FORBIDDEN)
        
        try:
            return_object = {
                'recipient_id': recipient_id,
                'recipient_name': serializers.RecipientSerializer(recipient, many=False).data['names'],
                'warehouse_address': serializers.WarehouseAddressSerializer(recipient.warehouse, many=False).data,
            }
        except Exception as e:
            return Response({'message': str(e), 'exception': type(e).__name__}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        return Response(return_object, status=status.HTTP_200_OK)