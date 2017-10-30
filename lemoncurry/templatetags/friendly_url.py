from django import template
from urllib.parse import urlparse

register = template.Library()


@register.filter
def friendly_url(url):
    (scheme, netloc, path, params, q, fragment) = urlparse(url)
    return netloc + path
