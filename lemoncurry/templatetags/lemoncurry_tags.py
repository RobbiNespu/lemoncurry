import json
from os.path import join
from types import SimpleNamespace

from django import template
from django.conf import settings
from django.urls import reverse

from .. import breadcrumbs
from entries import kinds

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
def request_origin(request):
    return '{scheme}://{host}'.format(
        scheme=request.scheme,
        host=request.META['HTTP_HOST'],
    )


@register.simple_tag
def request_uri(request):
    return request_origin(request) + request.path


@register.simple_tag
def site_name():
    return settings.LEMONCURRY_SITE_NAME


@register.inclusion_tag('lemoncurry/tags/nav.html')
def nav_left(request):
    items = (MenuItem(
        label=k.plural,
        icon=k.icon,
        url='entries:'+k.plural+'_index'
    ) for k in kinds.all)
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


@register.inclusion_tag('lemoncurry/tags/breadcrumbs.html', takes_context=True)
def nav_crumbs(context, route):
    crumbs = breadcrumbs.find(route)
    current = crumbs.pop()

    item_list_element = [{
        '@type': 'ListItem',
        'position': i + 1,
        'item': {
            '@id': context['origin'] + reverse(crumb['route']),
            '@type': 'WebPage',
            'name': crumb['label']
        }
    } for i, crumb in enumerate(crumbs)]
    item_list_element.append({
        '@type': 'ListItem',
        'position': len(item_list_element) + 1,
        'item': {
            'id': context['uri'],
            '@type': 'WebPage',
            'name': current['label'] or context.get('title'),
        }
    })

    breadcrumb_list = {
        '@context': 'http://schema.org',
        '@type': 'BreadcrumbList',
        'itemListElement': item_list_element
    }

    return {
        'breadcrumb_list': breadcrumb_list,
        'crumbs': crumbs,
        'current': current,
        'title': context['title'],
    }
