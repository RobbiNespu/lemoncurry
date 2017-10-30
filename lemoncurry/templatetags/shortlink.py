from django import template
from django.template import Context
from lemoncurry import utils

register = template.Library()


@register.simple_tag
def shortlink(obj):
    return utils.shortlink(obj)
