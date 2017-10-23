from .base import *
from .base import DATABASES

ALLOWED_HOSTS = ['00dani.me']
DATABASES['default'] = {
    'ENGINE': 'django.db.backends.postgresql',
    'NAME': 'lemoncurry',
    'USER': 'lemoncurry',
}
STATIC_URL = 'https://cdn.00dani.me/'
MEDIA_URL = STATIC_URL + 'media/'
