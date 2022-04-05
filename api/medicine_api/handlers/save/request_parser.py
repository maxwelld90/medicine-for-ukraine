import json
import dotmap
import ipware
from jsonschema import validate
from jsonschema import FormatChecker
from jsonschema.exceptions import ValidationError

class ImproperlyFormattedBodyError(Exception):
    pass

class ValidationFailureError(Exception):
    pass


REQUEST_SCHEMA = {
    'type': 'object',
    'properties': {
        'user_agent': {
            'description': 'The users\'s browser agent string',
            'type': 'string',
        },
        'recipient_id': {
            'description': 'ID of the recipient to send items to',
            'type': 'string',
            'format': 'uuid',
        },
        'selected': {
            'type': 'array',
            'items': {
                '$ref': '/schemas/store',
            }
        }
    },
    'required': [
        'user_agent',
        'recipient_id',
    ],

    '$defs': {
        'store': {
            '$id': '/schemas/store',
            'type': 'object',
            'properties': {
                'store_domain': {
                    'description': 'The domain of the store the item(s) has/have been purchased from',
                    'type': 'string',
                    'format': 'hostname',
                },
                'screenshots': {
                    'type': 'array',
                    'items': {
                        'description': 'The Base64 representation of the image',
                        'type': 'string',
                    },
                },
                'selected_items': {
                    'type': 'array',
                    'items': {
                        '$ref': '/schemas/item',
                    }
                }
            },
            'required': [
                'store_domain',
                'screenshots',
                'selected_items',
            ]
        },
        'item': {
            '$id': '/schemas/item',
            'type': 'object',
            'properties': {
                'url': {
                    'description': 'The URL to the item on the online shop',
                    'type': 'string',
                    'format': 'uri',
                },
                'name': {
                    'description': 'The name (in EN) of the item',
                    'type': 'string'
                },
                'quantity': {
                    'description': 'The number of the given item ordered',
                    'type': 'integer',
                },
                'row_number': {
                    'description': 'The row number from the sheet for the item selected',
                    'type': 'integer',
                }
            },
            'required': [
                'url',
                'name',
                'quantity',
                'row_number',
            ]
        }
    }
}


def get_client_ip(request):
    """
    Using django-ipware, attempts to retrieve the IP address of the client.
    Adapted from https://stackoverflow.com/a/16203978
    """
    ip, is_routable = ipware.get_client_ip(request)

    if ip is None:
        return None

    return ip


class RequestParser(object):
    """
    Class that represents a complete request's body.
    Access the data using dot notation from data, i.e., data.user_agent.
    """
    def __init__(self, request):
        self.__parse(request.body)
    
    def __parse(self, body):
        """
        Takes the response string (body), and instantiates the instance.
        """
        try:
            json_data = json.loads(body)
        except ValueError as e:
            raise ImproperlyFormattedBodyError(e)
        
        # Validate the JSON - if it doesn't match the schema above, an exception is raised.
        # These exceptions should be handled by the calling class.
        try:
            validate(instance=json_data, schema=REQUEST_SCHEMA, format_checker=FormatChecker())
        except ValidationError as e:
            raise ValidationFailureError(e)
        except ValueError as e:
            raise ValidationFailureError(e)
        
        # If we get here, the request is valid - make the data available through self.data.
        self.data = dotmap.DotMap(json_data)