"""
Django settings for lemoncurry project.

Generated by 'django-admin startproject' using Django 1.11.6.

For more information on this file, see
https://docs.djangoproject.com/en/1.11/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.11/ref/settings/
"""

import os
import re


# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.11/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '6riil57g@r^wprf7mdy((+bs&(6l*phcn9&fd$l0@t-kzj+xww'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = []
INTERNAL_IPS = ['127.0.0.1', '::1']

# Settings to tighten up security - these can safely be on in dev mode too,
# since I dev using a local HTTPS server.

# Strict-Transport-Security: max out everything, we never want to serve
# anything over insecure HTTP.
SECURE_HSTS_SECONDS = 31536000
SECURE_HSTS_INCLUDE_SUBDOMAINS = True
SECURE_HSTS_PRELOAD = True

# Only allow cookies to be sent from the client over secure HTTP.
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True

# Miscellanous headers to protect against attacks.
SECURE_CONTENT_TYPE_NOSNIFF = True
SECURE_BROWSER_XSS_FILTER = True
X_FRAME_OPTIONS = 'DENY'

# This technically isn't needed, since nginx doesn't let the app be accessed
# over insecure HTTP anyway. Just for completeness!
SECURE_SSL_REDIRECT = True

# We run behind nginx, so we need nginx to tell us whether we're using HTTPS or
# not.
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')

# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.admindocs',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.humanize',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.sitemaps',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    'analytical',
    'annoying',
    'compressor',
    'computed_property',
    'corsheaders',
    'debug_toolbar',
    'django_activeurl',
    'django_agent_trust',
    'django_otp',
    'django_otp.plugins.otp_totp',
    'django_rq',
    'favicon',
    'meta',

    'lemoncurry',
    'entries',
    'home',
    'lemonauth',
    'lemonshort',
    'micropub',
    'users',
    'webmention',
    'wellknowns',
]

MIDDLEWARE = [
    'debug_toolbar.middleware.DebugToolbarMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.admindocs.middleware.XViewMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django_otp.middleware.OTPMiddleware',
    'django_agent_trust.middleware.AgentMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.contrib.sites.middleware.CurrentSiteMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'lemoncurry.urls'

SESSION_ENGINE = 'django.contrib.sessions.backends.cached_db'

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

WSGI_APPLICATION = 'lemoncurry.wsgi.application'

# Cache
# https://docs.djangoproject.com/en/1.11/ref/settings/#std:setting-CACHES

CACHES = {
    'default': {
        'BACKEND': 'django_redis.cache.RedisCache',
        'LOCATION': 'redis://127.0.0.1:6380/0',
        'KEY_PREFIX': 'lemoncurry',
        'OPTIONS': {
            'PARSER_CLASS': 'redis.connection.HiredisParser',
            'SERIALIZER': 'django_redis.serializers.msgpack.MSGPackSerializer',
        },
        'VERSION': 2,
    }
}

# Database
# https://docs.djangoproject.com/en/1.11/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}


AUTH_USER_MODEL = 'users.User'

# Password hashers
# https://docs.djangoproject.com/en/1.11/ref/settings/#auth-password-validators
PASSWORD_HASHERS = [
    'django.contrib.auth.hashers.Argon2PasswordHasher',
    'django.contrib.auth.hashers.PBKDF2PasswordHasher',
    'django.contrib.auth.hashers.PBKDF2SHA1PasswordHasher',
    'django.contrib.auth.hashers.BCryptSHA256PasswordHasher',
    'django.contrib.auth.hashers.BCryptPasswordHasher',
]

# Password validation
# https://docs.djangoproject.com/en/1.11/ref/settings/#auth-password-validators

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

LOGIN_URL = 'lemonauth:login'
LOGIN_REDIRECT_URL = 'home:index'
LOGOUT_REDIRECT_URL = LOGIN_REDIRECT_URL


# Internationalization
# https://docs.djangoproject.com/en/1.11/topics/i18n/

LANGUAGE_CODE = 'en-au'

TIME_ZONE = 'Australia/Sydney'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.11/howto/static-files/

STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'static')
STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
    'compressor.finders.CompressorFinder',
)

COMPRESS_PRECOMPILERS = (
    ('text/stylus', './node_modules/.bin/stylus {infile} -u ./lemoncurry/static/lemoncurry/css/theme -o {outfile}'),
)

MEDIA_URL = STATIC_URL + 'media/'
MEDIA_ROOT = os.path.join(STATIC_ROOT, 'media')

# django-contrib-sites
# https://docs.djangoproject.com/en/dev/ref/contrib/sites/
SITE_ID = 1

# django-agent-trust
# https://pythonhosted.org/django-agent-trust/
AGENT_COOKIE_SECURE = True

# django-cors-headers
CORS_ORIGIN_ALLOW_ALL = True

# django-debug-toolbar
# https://django-debug-toolbar.readthedocs.io/en/stable/configuration.html
DEBUG_TOOLBAR_CONFIG = {
    'SHOW_TOOLBAR_CALLBACK': 'lemoncurry.debug.show_toolbar',
}

# lemonshort
SHORT_BASE_URL = '/s/'
SHORTEN_MODELS = {
    'e': 'entries.entry',
}

# django-meta
# https://django-meta.readthedocs.io/en/latest/settings.html
META_SITE_PROTOCOL = 'https'
META_USE_SITES = True
META_USE_OG_PROPERTIES = True
META_USE_TWITTER_PROPERTIES = True

# django-push
# https://django-push.readthedocs.io/en/latest/publisher.html
PUSH_HUB = 'https://00dani.superfeedr.com/'

# django-rq
# https://github.com/ui/django-rq
RQ_QUEUES = {'default': {'USE_REDIS_CACHE': 'default'}}

# django-super-favicon
FAVICON_STORAGE = 'django.core.files.storage.DefaultStorage'
