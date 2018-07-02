from django.http import JsonResponse
from django.urls import reverse
from lemoncurry import requests
from lemoncurry.middleware import ResponseException
from lemoncurry.utils import absolute_url
from . import error


def config(request):
    config = syndicate_to(request)
    config['media-endpoint'] = absolute_url(request, reverse('micropub:media'))
    return config


def source(request):
    get = request.GET
    if 'url' not in get:
        raise ResponseException(error.bad_req(
            'must specify url parameter for source query'
        ))
    mf2 = requests.mf2(get['url']).to_dict(filter_by_type='h-entry')
    if not mf2:
        raise ResponseException(error.bad_req('no h-entry at the requested url'))
    entry = mf2[0]
    keys = get.getlist('properties', []) + get.getlist('properties[]', [])
    if not keys:
        return entry

    props = entry['properties']
    return {'properties': {k: props[k] for k in keys if k in props}}


def syndicate_to(request):
    return {'syndicate-to': []}


queries = {
    'config': config,
    'source': source,
    'syndicate-to': syndicate_to,
}


def query(request):
    if 'q' not in request.GET:
        return error.bad_req('must specify q parameter')
    q = request.GET['q']
    if q not in queries:
        return error.bad_req('unsupported query {0}'.format(q))
    res = queries[q](request)
    return JsonResponse(res)
