import json
from django.conf import settings
from os.path import join
from types import SimpleNamespace

cache = SimpleNamespace(package_json=None)


def load_package_json():
    if cache.package_json:
        return cache.package_json
    with open(join(settings.BASE_DIR, 'package.json')) as f:
        cache.package_json = json.load(f)
    return cache.package_json


def origin(request):
    return '{0}://{1}'.format(request.scheme, request.META['HTTP_HOST'])


def uri(request):
    return origin(request) + request.path
