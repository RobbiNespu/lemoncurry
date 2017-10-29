from os import environ
from os.path import join

from .base import *
from .base import BASE_DIR, DATABASES

ALLOWED_HOSTS = ['00dani.me']
DEBUG = False
SECRET_KEY = environ['DJANGO_SECRET_KEY']

# Use Postgres instead of SQLite in production.
DATABASES['default'] = {
    'ENGINE': 'django.db.backends.postgresql',
    'NAME': 'lemoncurry',
    'USER': 'lemoncurry',
}

STATIC_ROOT = join(BASE_DIR, '..', 'static')
MEDIA_ROOT = join(BASE_DIR, '..', 'media')
STATIC_URL = 'https://cdn.00dani.me/'
MEDIA_URL = STATIC_URL + 'media/'
META_SITE_DOMAIN = '00dani.me'
META_FB_APPID = '145311792869199'
