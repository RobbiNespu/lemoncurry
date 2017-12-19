from django import template
from django.template.defaultfilters import stringfilter
from django.utils.safestring import mark_safe

from bleach.sanitizer import Cleaner, ALLOWED_TAGS
from bleach.linkifier import LinkifyFilter

tags = ['code', 'p', 'pre', 'img', 'span']
tags.extend(ALLOWED_TAGS)
attributes = {
    'a': ('href', 'title', 'class'),
    'img': ('alt', 'src', 'title'),
    'span': ('class',),
}

register = template.Library()
cleaner = Cleaner(tags=tags, attributes=attributes, filters=(LinkifyFilter,))


@register.filter
@stringfilter
def bleach(html):
    return mark_safe(cleaner.clean(html))
