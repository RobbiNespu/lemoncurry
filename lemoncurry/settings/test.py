from .base import *

ALLOWED_HOSTS = ['*']
SECURE_SSL_REDIRECT = False
STATICFILES_STORAGE = 'django.contrib.staticfiles.storage.StaticFilesStorage'

MEDIA_URL = '/media/'
STATIC_ROOT = path.join(BASE_DIR, 'media')
