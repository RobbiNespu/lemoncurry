import html
import json
from accept_types import get_best_match
from django.conf import settings
from django.http import HttpResponse, JsonResponse
from django.http import HttpResponseForbidden, HttpResponseBadRequest
from django.utils.html import strip_tags
from os.path import join
from types import SimpleNamespace
from urllib.parse import urlencode, urljoin, urlparse

from .templatetags.markdown import markdown

cache = SimpleNamespace(package_json=None)


def friendly_url(url):
    (scheme, netloc, path, params, q, fragment) = urlparse(url)
    return netloc + path


def load_package_json():
    if cache.package_json:
        return cache.package_json
    with open(join(settings.BASE_DIR, 'package.json')) as f:
        cache.package_json = json.load(f)
    return cache.package_json


def origin(request):
    return '{0}://{1}'.format(request.scheme, request.site.domain)


def absolute_url(request, url):
    return urljoin(origin(request), url)


def uri(request):
    return origin(request) + request.path


def form_encoded_response(content):
    return HttpResponse(
        urlencode(content),
        content_type='application/x-www-form-urlencoded'
    )


REPS = {
    'application/x-www-form-urlencoded': form_encoded_response,
    'application/json': JsonResponse,
}


def choose_type(request, content, reps=REPS):
    accept = request.META.get('HTTP_ACCEPT', '*/*')
    type = get_best_match(accept, reps.keys())
    if type:
        return reps[type](content)
    return HttpResponse(status=406)


def bad_req(message):
    return HttpResponseBadRequest(message, content_type='text/plain')


def forbid(message):
    return HttpResponseForbidden(message, content_type='text/plain')


def to_plain(md):
    return html.unescape(strip_tags(markdown(md)))
