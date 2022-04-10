import base64
from urllib.request import Request
import tldextract
from django.urls import reverse
from django.conf import settings
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from django.core.mail import EmailMessage
from django.core.files.base import ContentFile
from django.template.loader import get_template
from medicine_api.handlers.save import request_parser
from medicine_api.models import LinkMetadata, Recipient, RequestedItem, Screenshot, StoreSession, UserRequest


def create_screenshot_file(data, screenshot_object):
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
            return Response({'message': str(e), 'exception': 'ImproperlyFormattedBodyError'}, status=status.HTTP_400_BAD_REQUEST)
        except request_parser.ValidationFailureError as e:
            return Response({'message': str(e), 'exception': 'ValidationFailureError'}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({'message': str(e), 'exception': type(e).__name__}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        client_ip = request_parser.get_client_ip(request)

        try:
            user_request_object = self.__create_user_request(parser, client_ip)
            self.__create_store_metaitems(parser, user_request_object)
        except Recipient.DoesNotExist:
            return Response({'message': 'The recipient with the given ID does not exist', 'exception': 'DoesNotExist'}, status=status.HTTP_404_NOT_FOUND)
        except LinkMetadata.DoesNotExist as e:
            # If we get here, there was a URL that we haven't recognised.
            user_request_object.delete()
            return Response({'message': 'A link was not recognised.', 'exception': 'DoesNotExist'}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({'message': str(e), 'exception': type(e).__name__}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
        self.__send_email(request, parser, user_request_object)
        
        return Response({
            'recipient_id': parser.data.recipient_id,
            'user_request_id': user_request_object.id,
        }, status=status.HTTP_201_CREATED)
    
    def __send_email(self, request, parser, user_request_object):
        """
        Sends an e-mail to the recipient to alert them of the new request (if an e-mail address exists).
        If an e-mail address does not exist, None is returned.
        """
        recipient = Recipient.objects.get(id=parser.data.recipient_id)
        items = RequestedItem.objects.filter(store_session__user_request=user_request_object)
        screenshots = Screenshot.objects.filter(store_session__user_request=user_request_object)

        if recipient.email is not None:
            message_body = get_template('emails/request_submitted.html').render({
                'user_request': user_request_object,
                'items': items,
                'media_url': settings.MEDIA_URL,
                'screenshots': screenshots,
                'change_url': request.build_absolute_uri(reverse('admin:medicine_api_userrequest_change', kwargs={'object_id': user_request_object.id})),
            })

            email_object = EmailMessage(
                subject=f'{settings.SUBJECT_EMAIL_PREFIX} Order placed for item(s)',
                body=message_body,
                from_email=settings.AUTOMATED_EMAIL,
                to=[recipient.email],
            )

            email_object.content_subtype = 'plain'
            return email_object.send()
        
        return None
    
    def __create_user_request(self, parser, client_ip):
        """
        Creates and saves a new UserRequest object.
        Returns the new object once created.
        """
        recipient = Recipient.objects.get(id=parser.data.recipient_id)

        user_request_object = UserRequest(  # Remaining fields are populated automatically
            ip_address = client_ip,
            user_agent = parser.data.user_agent,
            recipient = recipient,
        )

        user_request_object.save()
        return user_request_object
    
    def __create_store_metaitems(self, parser, user_request_object):
        """
        Iterates over the parser's data to create store items and item references.
        Also creates screenshots for each store.
        """
        for store_data in parser.data.selected:
            store_domain = tldextract.extract(store_data.store_domain)
            
            # The domain may have already been processed; check for this (with a blank domain)
            if store_domain.domain == '':
                store_domain = store_domain.suffix
            else:
                store_domain = f'{store_domain.domain}.{store_domain.suffix}'

            # Create the store's session object.
            store_session_object = StoreSession(
                user_request = user_request_object,
                store_domain = store_domain,
            )

            store_session_object.save()

            for item_data in store_data.selected_items:
                link_metadata = LinkMetadata.objects.get(url=item_data.url)

                # For each selected item in the given store, create a reference.
                requested_item_object = RequestedItem(
                    store_session = store_session_object,
                    url = link_metadata,
                    name = item_data.name,
                    quantity = item_data.quantity,
                    row_number = item_data.row_number,
                    price_at_purchase = link_metadata.price,
                )

                requested_item_object.save()
            
            # For each of the store's screenshots in this session, save them.
            # Take the Base64 encoding, and save it as a file.
            for screenshot_data in store_data.screenshots:
                screenshot_object = Screenshot(
                    store_session = store_session_object,
                )

                # We need to save the incomplete screenshot object to get the ID for it.
                # This ID is used as the filename of the uploaded image file.
                screenshot_object.save()
                content_file = create_screenshot_file(screenshot_data, screenshot_object)

                screenshot_object.image = content_file
                screenshot_object.save()