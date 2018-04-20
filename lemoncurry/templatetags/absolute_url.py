from django import template
from django.contrib.sites.models import Site
from urllib.parse import urljoin

register = template.Library()


@register.simple_tag
@register.filter(is_safe=True)
def absolute_url(url):
    base = 'https://' + Site.objects.get_current().domain
    return urljoin(base, url)
