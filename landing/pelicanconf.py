import os
import sys
sys.path.append(os.curdir)

import languages

AUTHOR = 'Medicine for Ukraine Team'
SITENAME = 'Medicine for Ukraine'

# In what directory does the project content live?
PATH = 'content'

# Feed generation is usually not desired when developing
# Set these to None to avoid creating extra content in the output directory
FEED_ALL_ATOM = None
CATEGORY_FEED_ATOM = None
TRANSLATION_FEED_ATOM = None
AUTHOR_FEED_ATOM = None
AUTHOR_FEED_RSS = None

DEFAULT_PAGINATION = False

# Removes the other templates from output (e.g., authors, tags, etc.)
DIRECT_TEMPLATES = ['index']

# TEMPLATE_PAGES = {
#     'templates/page.html': 'index.html',
# }

# Places each generated HTML page in its own subdirectory, removing the need for .html.
PAGE_URL = '{slug}/'
PAGE_SAVE_AS = '{slug}/index.html'

THEME = './theme/'  # Path to theme directory (in the project root)
THEME_STATIC_DIR = 'static'  # Path for the output static directory

SITEURL = 'http://127.0.0.1:3000/'  # https://medicineforukraine.org/
STATIC_URL = '/static/'  # https://static.medicineforukraine.org/

ROOT_URL = SITEURL  # Make a copy of SITEURL so we have the absolute root of the project (for language switching)
SITEURL_ABSOLUTE = SITEURL

# Where do plugins live?
PLUGIN_PATHS = ['./plugins/']
PLUGINS = ['i18n_subsites', 'medicine_helpers']

# Localisation information (DEFAULT_LANG is the landing language)
TIMEZONE = 'Europe/London'
DEFAULT_LANG = 'en'
I18N_SUBSITES = languages.get_pelican_languages_object(SITEURL)

SITELINKS = I18N_SUBSITES['en']['SITELINKS']