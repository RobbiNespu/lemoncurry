from django.apps import apps
from django.conf import settings
from typing import Any, Dict, Type

from .convert import id_to_abc

prefixes = {}  # type: Dict[Type[Any], str]


def short_url(entity):
    if not prefixes:
        for k, m in settings.SHORTEN_MODELS.items():
            prefixes[apps.get_model(m)] = k
    base = '/'
    if hasattr(settings, 'SHORT_BASE_URL'):
        base = settings.SHORT_BASE_URL
    return base + prefixes[type(entity)] + id_to_abc(entity.id)
