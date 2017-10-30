from django import template
from urllib.parse import urlunparse, urlparse

register = template.Library()


@register.filter
def friendly_url(url):
    (scheme, netloc, path, params, q, fragment) = urlparse(url)
    return urlunparse(('', netloc, path, '', '', ''))
