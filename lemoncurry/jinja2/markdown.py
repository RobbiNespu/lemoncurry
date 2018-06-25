from jinja2 import evalcontextfilter
from markdown import Markdown

from .bleach import bleach

md = Markdown(extensions=(
    'markdown.extensions.extra',
    'markdown.extensions.headerid',
    'markdown.extensions.sane_lists',
    'markdown.extensions.smarty',
))


@evalcontextfilter
def markdown(ctx, source):
    return bleach(ctx, md.reset().convert(source))
