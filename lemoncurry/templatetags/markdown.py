from django import template

from markdown import Markdown
from .bleach import bleach

md = Markdown(extensions=(
    'extra',
    'sane_lists',
    'smarty',
    'toc',
))

register = template.Library()


@register.filter
def markdown(source):
    return bleach(md.reset().convert(source))
