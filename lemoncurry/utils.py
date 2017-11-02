import json
from accept_types import get_best_match
from django.conf import settings
from django.http import HttpResponse
from django.http import HttpResponseForbidden, HttpResponseBadRequest
from os.path import join
from shorturls import default_converter as converter
from shorturls.templatetags.shorturl import ShortURL
from types import SimpleNamespace
from urllib.parse import urlencode, urljoin

cache = SimpleNamespace(package_json=None)


def load_package_json():
    if cache.package_json:
        return cache.package_json
    with open(join(settings.BASE_DIR, 'package.json')) as f:
        cache.package_json = json.load(f)
    return cache.package_json


def origin(request):
    return '{0}://{1}'.format(request.scheme, request.site.domain)


def uri(request):
    return origin(request) + request.path


def choose_type(request, content, reps):
    accept = request.META.get('HTTP_ACCEPT', '*/*')
    type = get_best_match(accept, reps.keys())
    if type:
        return reps[type](content)
    return HttpResponse(status=406)


def form_encoded_response(content):
    return HttpResponse(
        urlencode(content),
        content_type='application/x-www-form-urlencoded'
    )


def shortlink(obj):
    prefix = ShortURL(None).get_prefix(obj)
    tinyid = converter.from_decimal(obj.pk)
    if hasattr(settings, 'SHORT_BASE_URL') and settings.SHORT_BASE_URL:
        return urljoin(settings.SHORT_BASE_URL, prefix + tinyid)
    return '/' + prefix + tinyid


def bad_req(message):
    return HttpResponseBadRequest(message, content_type='text/plain')


def forbid(message):
    return HttpResponseForbidden(message, content_type='text/plain')
