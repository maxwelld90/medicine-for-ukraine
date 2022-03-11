import json
from re import M
from jsonschema import validate
from jsonschema import FormatChecker
from jsonschema.exceptions import ValidationError
from api_app.models import Address, Country

class ImproperlyFormattedBodyError(Exception):
    pass

class ValidationFailureError(Exception):
    pass


REQUEST_SCHEMA = {
    'type': 'object',
    'properties': {
        'email': {
            'description': 'The user\'s e-mail address',
            'type': 'string',
            'format': 'email',
        },
        'country_to_deliver': {
            'description': 'Country code for delivery',
            'type': 'string',
            'enum': [country.code for country in Country.objects.all()]  # Get a series of countries from the database to compare against
        },
        'address': {
            'description': 'ID of address to deliver to',
            'type': 'integer',
            'enum': [address.id for address in Address.objects.all()]  # Get the IDs of addresses that are currently active!
        },
        'selected': {
            'type': 'array',
            'items': {
                '$ref': '/schemas/store',
            }
        }
    },
    'required': [
        'email',
        'country_to_deliver',
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
                'screenshot': {
                    'description': 'Base64 representation of the screenshot for the given store',
                    'type': 'string',
                },
                'items': {
                    'type': 'array',
                    'items': {
                        '$ref': '/schemas/item'
                    }
                }
            },
            'required': [
                'store_domain',
                'screenshot',
                'items'
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
                }
            },
            'required': [
                'url',
                'name',
                'quantity',
            ]
        }
    }
}

class RequestParser(object):
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

        try:
            validate(instance=json_data, schema=REQUEST_SCHEMA, format_checker=FormatChecker())
        except ValidationError as e:
            raise ValidationFailureError(e)
        except ValueError as e:
            raise ValidationFailureError(e)