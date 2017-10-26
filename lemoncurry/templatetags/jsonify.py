from django import template
from django.core.serializers import serialize
from django.core.serializers.json import DjangoJSONEncoder
from django.db.models.query import QuerySet
from django.utils.safestring import mark_safe
import json

register = template.Library()


@register.filter
def jsonify(value):
    if isinstance(value, QuerySet):
        return mark_safe(serialize('json', value))
    return mark_safe(json.dumps(value, cls=DjangoJSONEncoder))
