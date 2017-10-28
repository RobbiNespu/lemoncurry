from django import template
from ..theme import color

register = template.Library()


@register.simple_tag
def theme_colour(i):
    return color(i)
