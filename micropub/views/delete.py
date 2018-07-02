from django.http import HttpResponse
from django.urls import resolve, Resolver404
from urllib.parse import urlparse

from entries.jobs import ping_hub
from entries.models import Entry

from . import error

def delete(request):
    normalise = {
        'application/json': lambda r: r.json.get('url'),
        'application/x-www-form-urlencoded': lambda r: r.POST.get('url'),
    }
    if 'delete' not in request.token:
        return error.bad_scope('delete')
    if request.content_type not in normalise:
        return error.unsupported_type(request.content_type)
    url = normalise[request.content_type](request)
    if not url:
        return error.bad_req('url parameter required')

    if '//' not in url:
        url = '//' + url
    url = urlparse(url, scheme='https')

    if url.scheme not in ('http', 'https') or url.netloc != request.site.domain:
        return error.bad_req('url does not point to this site')
    try:
        match = resolve(url.path)
    except Resolver404:
        return error.bad_req('url does not point to a valid page on this site')

    if match.view_name != 'entries:entry':
        return error.bad_req('url does not point to an entry on this site')

    try:
        entry = Entry.objects.get(pk=match.kwargs['id'])
    except Entry.DoesNotExist:
        return error.bad_req('url does not point to an existing entry')

    if entry.author != request.token.user:
        return error.forbid('entry belongs to another user')

    urls = entry.affected_urls
    entry.delete()
    ping_hub.delay(urls)
    return HttpResponse(status=204)
