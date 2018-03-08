from django.conf.urls import url
from django.urls import reverse
from . import kinds
from .views import feeds, lists, perma
from lemoncurry import breadcrumbs as crumbs


def to_pat(*args):
    return '^{0}$'.format(''.join(args))


def prefix(route):
    return app_name + ':' + route


id = r'/(?P<id>\d+)'
kind = r'(?P<kind>{0})'.format('|'.join(k.plural for k in kinds.all))
page = r'(?:/page/(?P<page>\d+))?'
slug = r'/(?P<slug>[^/]+)'

slug_opt = '(?:' + slug + ')?'

app_name = 'entries'
urlpatterns = (
    url('^atom$', feeds.AtomHomeEntries(), name='atom'),
    url('^rss$', feeds.RssHomeEntries(), name='rss'),
    url(to_pat('cats', slug, page), lists.by_cat, name='cat'),
    url(to_pat(kind, page), lists.by_kind, name='index'),
    url(to_pat(kind, '/atom'), feeds.AtomByKind(), name='atom_by_kind'),
    url(to_pat(kind, '/rss'), feeds.RssByKind(), name='rss_by_kind'),
    url(to_pat(kind, id, slug_opt, '/amp'), perma.entry_amp, name='entry_amp'),
    url(to_pat(kind, id, slug_opt), perma.entry, name='entry'),
)


class IndexCrumb(crumbs.Crumb):
    def __init__(self):
        super().__init__(prefix('index'), parent='home:index')

    @property
    def label(self):
        return self.match.kwargs['kind']

    @property
    def url(self):
        return reverse(prefix('index'), kwargs={'kind': self.label})


crumbs.add(prefix('cat'), parent='home:index')
crumbs.add(IndexCrumb())
crumbs.add(prefix('entry'), parent=prefix('index'))
