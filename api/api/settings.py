"""
Django settings for api project.

Generated by 'django-admin startproject' using Django 4.0.3.

For more information on this file, see
https://docs.djangoproject.com/en/4.0/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/4.0/ref/settings/
"""

import os
from pathlib import Path

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'DEBUG_KEY'

if os.getenv('MEDICINE_ENVIRONMENT') == 'production':
    SECRET_KEY = os.getenv('MEDICINE_DJANGOKEY')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False

if os.getenv('MEDICINE_DEBUG') == 'true':
    DEBUG = True

if os.getenv('MEDICINE_ENVIRONMENT') == 'production':
    ALLOWED_HOSTS = ['api.medicineforukraine.org']
else:
    ALLOWED_HOSTS = ['*']


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'rest_framework',
    'corsheaders',
    'api_app',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

CORS_ALLOWED_ORIGINS = [
    "https://medicineforukraine.org",
    "http://localhost:3000",
    "http://127.0.0.1:3000",
]

DATA_UPLOAD_MAX_MEMORY_SIZE = 50 * 1024 * 1024

ROOT_URLCONF = 'api.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'api.wsgi.application'


# Database
# https://docs.djangoproject.com/en/4.0/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

if os.getenv('MEDICINE_ENVIRONMENT') == 'production':
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.postgresql_psycopg2',
            'NAME': os.getenv('MEDICINE_DB_NAME'),
            'USER': os.getenv('MEDICINE_DB_USER'),
            'PASSWORD': os.getenv('MEDICINE_DB_PASSWORD'),
            'HOST': '127.0.0.1',
            'PORT': '5432',
        }
    }


# Password validation
# https://docs.djangoproject.com/en/4.0/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]


# Internationalization
# https://docs.djangoproject.com/en/4.0/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.0/howto/static-files/

STATIC_URL = 'static/'

MEDIA_URL = 'uploads/'
MEDIA_ROOT = os.path.join(Path(__file__).resolve().parent.parent.parent, 'uploads')

if os.getenv('MEDICINE_ENVIRONMENT') == 'production':
    STATIC_URL = 'https://static.medicineforukraine.org/'
    STATIC_ROOT = '/srv/medicine-for-ukraine/static/'
    STATICFILES_DIRS = (
        '/srv/medicine-for-ukraine/virtualenv/lib/python3.8/site-packages/django/contrib/admin/static',
    )

    MEDIA_URL = 'https://media.medicineforukraine.org/'
    MEDIA_ROOT = '/srv/medicine-for-ukraine/uploads/'

# Default primary key field type
# https://docs.djangoproject.com/en/4.0/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

if os.getenv('MEDICINE_DEBUG') != 'true':
    REST_FRAMEWORK = {
        'DEFAULT_RENDERER_CLASSES': (
            'rest_framework.renderers.JSONRenderer',
        )
    }

if os.getenv('MEDICINE_ENVIRONMENT') == 'production':
    GOOGLE_API_SECRET_PATH = '/srv/medicine-for-ukraine/google_api_secret.json'
else:
    GOOGLE_API_SECRET_PATH = os.path.join(Path(__file__).resolve().parent.parent.parent, 'client_secret.json')

EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

if os.getenv('MEDICINE_ENVIRONMENT') == 'production' and not os.getenv('MEDICINE_DEBUG') == 'true':
    EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
    EMAIL_HOST = 'localhost'
    EMAIL_PORT = 25
    EMAIL_HOST_USER = ''
    EMAIL_HOST_PASSWORD = ''
    EMAIL_USE_TLS = False
    DEFAULT_FROM_EMAIL = 'Medicine for Ukraine <noreply@medicineforukraine.org>'