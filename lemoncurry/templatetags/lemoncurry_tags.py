
from django import template
from django.conf import settings
from django.contrib.sites.models import Site
from django.urls import reverse
from ..utils import load_package_json, origin, uri

from .. import breadcrumbs
from entries import kinds

register = template.Library()


class MenuItem:
    def __init__(self, label, icon, url):
        self.label = label
        self.icon = icon
        if isinstance(url, str):
            url = (url, ())
        self.url = reverse(url[0], args=url[1])


@register.simple_tag
def get_package_json():
    return load_package_json()


@register.simple_tag
def request_origin(request):
    return origin(request)


@register.simple_tag
def request_uri(request):
    return uri(request)


@register.simple_tag
def site_name():
    return Site.objects.get_current().name


@register.inclusion_tag('lemoncurry/tags/nav.html')
def nav_left(request):
    items = (MenuItem(
        label=k.plural,
        icon=k.icon,
        url=('entries:index', (k.plural,))
    ) for k in kinds.all)
    return {'items': items, 'request': request}


@register.inclusion_tag('lemoncurry/tags/nav.html')
def nav_right(request):
    if request.user.is_authenticated():
        items = (
            MenuItem(label='admin', icon='fas fa-cog', url='admin:index'),
            MenuItem(label='log out', icon='fas fa-sign-out-alt', url='lemonauth:logout'),
        )
    else:
        items = (
            MenuItem(label='log in', icon='fas fa-sign-in-alt', url='lemonauth:login'),
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
            '@id': context['origin'] + crumb.url,
            '@type': 'WebPage',
            'name': crumb.label
        }
    } for i, crumb in enumerate(crumbs)]
    item_list_element.append({
        '@type': 'ListItem',
        'position': len(item_list_element) + 1,
        'item': {
            'id': context['uri'],
            '@type': 'WebPage',
            'name': current.label or context.get('title'),
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
        'title': context.get('title'),
    }


@register.simple_tag
def get_push_hub():
    return settings.PUSH_HUB
