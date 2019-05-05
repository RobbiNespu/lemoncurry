from bleach.sanitizer import Cleaner, ALLOWED_TAGS
from bleach.linkifier import LinkifyFilter
from jinja2 import evalcontextfilter, Markup

TAGS = ['cite', 'code', 'details', 'p', 'pre', 'img', 'span', 'summary']
TAGS.extend(ALLOWED_TAGS)
ATTRIBUTES = {
    'a': ('href', 'title', 'class'),
    'details': ('open',),
    'img': ('alt', 'src', 'title'),
    'span': ('class',),
}

cleaner = Cleaner(tags=TAGS, attributes=ATTRIBUTES, filters=(LinkifyFilter,))


@evalcontextfilter
def bleach(ctx, html):
    res = cleaner.clean(html)
    if ctx.autoescape:
        res = Markup(res)
    return res
