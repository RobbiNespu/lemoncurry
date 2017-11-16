import requests
from cachecontrol.wrapper import CacheControl
from cachecontrol.cache import BaseCache
from cachecontrol.heuristics import LastModified
from datetime import datetime
from django.core.cache import cache as django_cache
from hashlib import sha256
from mf2py import Parser


class DjangoCache(BaseCache):
    @classmethod
    def key(cls, url):
        return 'req:' + sha256(url.encode('utf-8')).hexdigest()

    def get(self, url):
        key = self.key(url)
        return django_cache.get(key)

    def set(self, url, value, expires=None):
        key = self.key(url)
        if expires:
            lifetime = (expires - datetime.utcnow()).total_seconds()
            django_cache.set(key, value, lifetime)
        else:
            django_cache.set(key, value)

    def delete(self, url):
        key = self.key(url)
        django_cache.delete(key)


req = CacheControl(
    requests.Session(),
    cache=DjangoCache(),
    heuristic=LastModified(),
)


def get(url):
    r = req.get(url)
    r.raise_for_status()
    return r


def mf2(url):
    r = get(url)
    return Parser(doc=r.text, url=url, html_parser='html5lib')
