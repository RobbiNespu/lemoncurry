from jinja2 import evalcontextfilter
from markdown import Markdown

from .bleach import bleach

md = Markdown(extensions=(
    'extra',
    'sane_lists',
    'smarty',
    'toc',
))


@evalcontextfilter
def markdown(ctx, source):
    return bleach(ctx, md.reset().convert(source))
