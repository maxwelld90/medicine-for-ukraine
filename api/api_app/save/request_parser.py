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
        'browser_agent': {
            'description': 'The users\'s browser agent string',
            'type': 'string',
        },
        'ip_address': {
            'description': 'The user\'s IP address',
            'type': 'string',
            'format': 'ipv4',
        },
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
        'browser_agent',
        'ip_address',
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
                'screenshots': {
                    'type': 'array',
                    'items': {
                        'description': 'The Base64 representation of an image to be uploaded.',
                        'type': 'string',
                    },
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
                'screenshots',
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
                },
                'type': {
                    'description': 'The sheet from which the item comes from (e.g., meds/defence)',
                    'type': 'string',
                    'enum': ['meds', 'defence'],
                }
            },
            'required': [
                'url',
                'name',
                'quantity',
                'type',
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
        
        # https://stackoverflow.com/questions/38034377/object-like-attribute-access-for-nested-dictionary
        # Turn dict into object