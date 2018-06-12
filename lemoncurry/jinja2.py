from django.contrib.staticfiles.storage import staticfiles_storage
from django.urls import reverse
from jinja2 import Environment

from compressor.contrib.jinja2ext import CompressorExtension
from django_activeurl.ext.django_jinja import ActiveUrl

from entries.kinds import all as entry_kinds
from .utils import load_package_json


def environment(**options):
    env = Environment(
        extensions=[ActiveUrl, CompressorExtension],
        trim_blocks=True,
        lstrip_blocks=True,
        **options
    )
    env.globals.update({
        'entry_kinds': entry_kinds,
        'package': load_package_json(),
        'static': staticfiles_storage.url,
        'url': reverse,
    })
    return env
