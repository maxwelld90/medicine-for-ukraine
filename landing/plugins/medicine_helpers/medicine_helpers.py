import os
import logging

__all__ = [
    'link',
    'switch_language_link',
]

LOG_PREFIX = "[Medicine Helpers]"
logger = logging.getLogger(__name__)

def link(root, path):
    dir_name = f'{root}{os.path.dirname(path)}'

    if (dir_name[-1] != '/'):
        return f'{dir_name}/'

    return dir_name

def switch_language_link(value, language, path):
    dir_name = f'{value}{language}/{os.path.dirname(path)}'

    if (dir_name[-1] != '/'):
        return f'{dir_name}/'
    
    return dir_name