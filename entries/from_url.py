from urllib.parse import urlparse

from django.contrib.sites.models import Site
from django.http import HttpResponse
from django.urls import resolve, Resolver404
from micropub import error

from .models import Entry


def from_url(url: str) -> Entry:
    domain = Site.objects.get_current().domain
    if not url:
        raise error.bad_req('url parameter required')
    if '//' not in url:
        url = '//' + url
    parts = urlparse(url, scheme='https')
    if parts.scheme not in ('http', 'https') or parts.netloc != domain:
        raise error.bad_req('url does not point to this site')

    try:
        match = resolve(parts.path)
    except Resolver404:
        raise error.bad_req('url does not point to a valid page on this site')

    if match.view_name != 'entries:entry':
        raise error.bad_req('url does not point to an entry on this site')

    try:
        entry = Entry.objects.get(pk=match.kwargs['id'])
    except Entry.DoesNotExist:
        raise error.bad_req('url does not point to an existing entry')

    return entry
