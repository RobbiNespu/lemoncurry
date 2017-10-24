import json
from collections import namedtuple
from os.path import join
from types import SimpleNamespace

from django import template
from django.conf import settings
from django.urls import reverse

from .. import breadcrumbs

register = template.Library()
cache = SimpleNamespace(package_json=None)


class MenuItem:
    def __init__(self, label, icon, url):
        self.label = label
        self.icon = icon
        self.url = reverse(url)


@register.simple_tag
def get_package_json():
    if cache.package_json:
        return cache.package_json
    with open(join(settings.BASE_DIR, 'package.json')) as f:
        cache.package_json = json.load(f)
    return cache.package_json


@register.simple_tag
def request_uri(request):
    return '{scheme}://{host}{path}'.format(
        scheme=request.scheme,
        host=request.META['HTTP_HOST'],
        path=request.path
    )


@register.simple_tag
def site_name():
    return settings.LEMONCURRY_SITE_NAME


@register.inclusion_tag('lemoncurry/tags/nav.html')
def nav_left(request):
    items = ()
    return {'items': items, 'request': request}


@register.inclusion_tag('lemoncurry/tags/nav.html')
def nav_right(request):
    if request.user.is_authenticated():
        items = (
            MenuItem(label='admin', icon='fa fa-gear', url='admin:index'),
            MenuItem(label='log out', icon='fa fa-sign-out', url='lemonauth:logout'),
        )
    else:
        items = (
            MenuItem(label='log in', icon='fa fa-sign-in', url='lemonauth:login'),
        )
    return {'items': items, 'request': request}


@register.inclusion_tag('lemoncurry/tags/breadcrumbs.html')
def nav_crumbs(route):
    crumbs = breadcrumbs.find(route)
    current = crumbs.pop()
    return {'crumbs': crumbs, 'current': current}
