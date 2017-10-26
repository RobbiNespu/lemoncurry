from django import template

from markdown import Markdown
from .bleach import bleach

md = Markdown(extensions=(
    'markdown.extensions.extra',
    'markdown.extensions.headerid',
    'markdown.extensions.sane_lists',
    'markdown.extensions.smarty',
))

register = template.Library()


@register.filter
def markdown(source):
    return bleach(md.reset().convert(source))
