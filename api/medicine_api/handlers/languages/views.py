import json
from django.conf import settings
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response


class LanguageListing(APIView):
    """
    Returns a language listing, including the specification of the default language.
    """
    def get(self, request):
        try:
            with open('../LANGUAGES.json', 'r') as f:
                languages = json.load(f)
        
        except FileNotFoundError:
            return Response({'message': 'The languages file was not found.', 'exception': 'FileNotFoundError'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        except Exception as e:
            return Response({'message': str(e), 'exception': type(e).__name__}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        return_object = {
            'count': len(languages.keys()),
            'codes': languages.keys(),
            'default': settings.LANGUAGE_CODE,
            'sitenames': {language_code:language_data['SITENAME'] for (language_code,language_data) in languages.items()}
        }

        return Response(return_object, status=status.HTTP_200_OK)