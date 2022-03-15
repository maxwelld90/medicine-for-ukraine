import base64
import tldextract
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from django.core.files.base import ContentFile
from api_app.save import request_parser
from api_app.models import Address, Country, RequestedItem, Screenshot, StoreSession, UserRequest


class AddressMismatchError(Exception):
    pass

class AddressDisabledError(Exception):
    pass


def create_screenshot_file(data, screenshot_object=None):
    """
    Takes a Base64 raw string from the request's body, and creates a file object.
    Returns this object for saving.
    """
    img_format, base64_rep_str = data.split(';base64,')
    img_name, img_ext = img_format.split('/')

    return ContentFile(
        base64.b64decode(base64_rep_str),
        name = f'{str(screenshot_object.id)}.{img_ext}'
    )


class SaveRequest(APIView):
    def post(self, request):
        try:
            parser = request_parser.RequestParser(request)
        except request_parser.ImproperlyFormattedBodyError as e:
            return Response({'message': f'The JSON request was badly formed. {e}'}, status=status.HTTP_400_BAD_REQUEST)
        except request_parser.ValidationFailureError as e:
            return Response({'message': f'The data sent does not match what was expected. {e}'}, status.HTTP_400_BAD_REQUEST)

        # If we get here, the request is valid, and we should save it.
        client_ip = request_parser.get_client_ip(request)

        # There are some database integrity checks we also need to do here.
        # These are raised and handled here.
        try:
            user_request_object = self.create_user_request(parser, client_ip)
            self.create_store_items(parser, user_request_object)
        except Country.DoesNotExist:
            return Response({'message': f'The country code specified does not exist.'}, status=status.HTTP_404_NOT_FOUND)
        except Address.DoesNotExist:
            return Response({'message': f'The specified address does not exist.'}, status=status.HTTP_404_NOT_FOUND)
        except AddressMismatchError:
            return Response({'message': f'The specified address does not match the specified country.'}, status=status.HTTP_400_BAD_REQUEST)
        except AddressDisabledError:
            return Response({'message': f'The given address is not currently available.'}, status=status.HTTP_400_BAD_REQUEST)
        
        # HTTP 201 is the success code here: CREATED.
        return Response({}, status=status.HTTP_201_CREATED)
    
    def create_user_request(self, parser, client_ip):
        """
        Creates the UserRequest object, and saves it.
        Returns the new object.
        """
        selected_country = Country.objects.get(code=parser.data.country_to)
        selected_address = Address.objects.get(id=parser.data.address)

        if selected_address.country != selected_country:
            raise AddressMismatchError()
        
        if not selected_address.is_active:
            raise AddressDisabledError()

        user_request_object = UserRequest(  # Remaining fields are automatically generated.
            ip_address = client_ip,
            user_agent = parser.data.user_agent,
            email = parser.data.email,
            country_to = selected_country,
            address_to = selected_address,
        )

        user_request_object.save()
        return user_request_object
    
    def create_store_items(self, parser, user_request_object):
        """
        Iterates over the parser's data to create store items and item references.
        Also creates screenshots for each store.
        """
        for store_data in parser.data.selected:
            store_domain = tldextract.extract(store_data.store_domain)
            store_domain = f'{store_domain.domain}.{store_domain.suffix}'

            # Create the store's session object.
            store_session_object = StoreSession(
                user_request = user_request_object,
                store_domain = store_domain,
            )

            store_session_object.save()

            for item_data in store_data.selected_items:
                # For each selected item from the given store, create a reference.
                requested_item_object = RequestedItem(
                    store_session = store_session_object,
                    url = item_data.url,
                    name = item_data.name,
                    type = item_data.type,
                    quantity = item_data.quantity,
                    row_number = item_data.row_number,
                )

                requested_item_object.save()
            
            # For each of the store's screenshots in this session, save them.
            # Take the Base64 encoding and save it as a file.
            for screenshot_data in store_data.screenshots:
                screenshot_object = Screenshot(
                    store_session = store_session_object,
                )

                # We need to save the incomplete screenshot object to get the new ID for it.
                # This ID is used as the filename for the uploaded image file.
                screenshot_object.save()
                content_file = create_screenshot_file(screenshot_data, screenshot_object=screenshot_object)

                screenshot_object.image = content_file
                screenshot_object.save()