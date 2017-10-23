import json
from os.path import join
from types import SimpleNamespace

from django import template
from django.conf import settings

register = template.Library()
cache = SimpleNamespace(package_json=None)


@register.simple_tag
def get_package_json():
    if cache.package_json:
        return cache.package_json
    with open(join(settings.BASE_DIR, 'package.json')) as f:
        cache.package_json = json.load(f)
    return cache.package_json


@register.simple_tag
def site_name():
    return settings.LEMONCURRY_SITE_NAME
