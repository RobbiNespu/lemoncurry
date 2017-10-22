import json
from os.path import join

from django import template
from django.conf import settings

register = template.Library()


@register.simple_tag
def get_package_json():
    with open(join(settings.BASE_DIR, 'package.json')) as f:
        package = json.load(f)
    return package


@register.simple_tag
def site_name():
    return settings.LEMONCURRY_SITE_NAME
