import json
import dotmap
import ipware
from jsonschema import validate
from jsonschema import FormatChecker
from django.db.utils import OperationalError
from jsonschema.exceptions import ValidationError
from api_app.models import Address, Country

class ImproperlyFormattedBodyError(Exception):
    pass

class ValidationFailureError(Exception):
    pass

# Attempt to retrieve a list of Addresses and Countries; if this fails, the tables do not exist.
try:
    COUNTRIES = [country.code for country in Country.objects.all()]
    ADDRESSES = [address.id for address in Address.objects.all()]
except OperationalError:
    COUNTRIES = []
    ADDRESSES = []


REQUEST_SCHEMA = {
    'type': 'object',
    'properties': {
        'user_agent': {
            'description': 'The users\'s browser agent string',
            'type': 'string',
        },
        'email': {
            'description': 'The user\'s e-mail address',
            'type': 'string',
            'format': 'email',
        },
        'country_to': {
            'description': 'Country code for delivery',
            'type': 'string',
            'enum': COUNTRIES  # Get a series of countries from the database to compare against
        },
        'address': {
            'description': 'ID of address to deliver to',
            'type': 'integer',
            'enum': ADDRESSES  # Get the IDs of addresses that are currently active!
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
        'email',
        'country_to',
        'address',
        'selected',
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
                        'description': 'The Base64 representation of an image to be uploaded.',
                        'type': 'string',
                    },
                },
                'selected_items': {
                    'type': 'array',
                    'items': {
                        '$ref': '/schemas/item'
                    }
                }
            },
            'required': [
                'store_domain',
                'screenshots',
                'selected_items'
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
                'type': {
                    'description': 'The sheet from which the item comes from (e.g., meds/defence)',
                    'type': 'string',
                    'enum': ['meds', 'defence'],
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
                'type',
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