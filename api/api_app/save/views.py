from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from api_app.save import request_parser


class SaveRequest(APIView):
    def post(self, request):
        try:
            parser = request_parser.RequestParser(request)
        except request_parser.ImproperlyFormattedBodyError as e:
            return Response({'message': f'The JSON request was badly formed. {e}'}, status=status.HTTP_400_BAD_REQUEST)
        except request_parser.ValidationFailureError as e:
            return Response({'message': f'The data sent does not match what was expected. {e}'}, status.HTTP_400_BAD_REQUEST)
        
        return Response("OK so far", status=status.HTTP_200_OK)