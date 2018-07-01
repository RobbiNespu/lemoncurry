from django.contrib.staticfiles.storage import staticfiles_storage
from django.conf import settings
from django.urls import reverse
from jinja2 import Environment

from compressor.contrib.jinja2ext import CompressorExtension
from django_activeurl.ext.django_jinja import ActiveUrl

from entries.kinds import all as entry_kinds
from wellknowns.favicons import icons as favicons

from .ago import ago
from .markdown import markdown
from ..theme import color as theme_color
from ..utils import friendly_url, load_package_json


def environment(**options):
    env = Environment(
        extensions=[ActiveUrl, CompressorExtension],
        trim_blocks=True,
        lstrip_blocks=True,
        **options
    )
    env.filters.update({
        'ago': ago,
        'friendly_url': friendly_url,
        'markdown': markdown,
    })
    env.globals.update({
        'entry_kinds': entry_kinds,
        'favicons': favicons,
        'package': load_package_json(),
        'settings': settings,
        'static': staticfiles_storage.url,
        'theme_color': theme_color,
        'url': reverse,
    })
    return env
