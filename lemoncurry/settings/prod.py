from os import environ

from .base import *
from .base import DATABASES

ALLOWED_HOSTS = ['00dani.me']
DEBUG = False
SECRET_KEY = environ['DJANGO_SECRET_KEY']

# Use Postgres instead of SQLite in production.
DATABASES['default'] = {
    'ENGINE': 'django.db.backends.postgresql',
    'NAME': 'lemoncurry',
    'USER': 'lemoncurry',
}

STATIC_URL = 'https://cdn.00dani.me/'
MEDIA_URL = STATIC_URL + 'media/'
