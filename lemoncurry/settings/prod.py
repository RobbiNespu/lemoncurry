from os import environ
from os.path import join

from .base import *
from .base import BASE_DIR, DATABASES

ALLOWED_HOSTS = ['00dani.me']
DEBUG = False
SECRET_KEY = environ['DJANGO_SECRET_KEY']
SERVER_EMAIL = 'lemoncurry@00dani.me'

# Authenticate as an app-specific Postgres user in production.
DATABASES['default']['USER'] = 'lemoncurry'

SHORT_BASE_URL = 'https://nya.as/'

STATIC_ROOT = join(BASE_DIR, '..', 'static')
MEDIA_ROOT = join(BASE_DIR, '..', 'media')
STATIC_URL = 'https://cdn.00dani.me/'
MEDIA_URL = STATIC_URL + 'm/'
META_SITE_DOMAIN = '00dani.me'
META_FB_APPID = '145311792869199'
