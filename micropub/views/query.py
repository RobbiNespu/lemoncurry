from django.http import JsonResponse
from django.urls import reverse

from entries.from_url import from_url
from lemoncurry import requests
from lemoncurry.utils import absolute_url
from .. import error



def config(request):
    config = syndicate_to(request)
    config['media-endpoint'] = absolute_url(request, reverse('micropub:media'))
    return config


def source(request):
    if 'url' not in request.GET:
        raise error.bad_req('must specify url parameter for source query')
    entry = from_url(request.GET['url'])
    props = {}

    keys = set(request.GET.getlist('properties') + request.GET.getlist('properties[]'))
    if not keys or 'content' in keys:
        props['content'] = [entry.content]
    if (not keys or 'category' in keys) and entry.cats.exists():
        props['category'] = [cat.name for cat in entry.cats.all()]
    if (not keys or 'name' in keys) and entry.name:
        props['name'] = [entry.name]
    if (not keys or 'syndication' in keys) and entry.syndications.exists():
        props['syndication'] = [synd.url for synd in entry.syndications.all()]

    return {'type': ['h-entry'], 'properties': props}


def syndicate_to(request):
    return {'syndicate-to': []}


queries = {
    'config': config,
    'source': source,
    'syndicate-to': syndicate_to,
}


def query(request):
    if 'q' not in request.GET:
        raise error.bad_req('must specify q parameter')
    q = request.GET['q']
    if q not in queries:
        raise error.bad_req('unsupported query {0}'.format(q))
    res = queries[q](request)
    return JsonResponse(res)
