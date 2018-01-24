from django import template
from urllib.parse import urljoin
from ..utils import origin

register = template.Library()


@register.simple_tag(takes_context=True)
def absolute_url(context, url):
    return urljoin(origin(context.request), url)
