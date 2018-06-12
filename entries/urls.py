from django.urls import path, register_converter, reverse
from . import kinds
from .views import feeds, lists, perma
from lemoncurry import breadcrumbs as crumbs

register_converter(kinds.EntryKindConverter, 'kind')


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
    path('atom', feeds.AtomHomeEntries(), name='atom'),
    path('rss', feeds.RssHomeEntries(), name='rss'),
    path('cats/<slug:slug>', lists.by_cat, name='cat'),
    path('cats/<slug:slug>/page/<int:page>', lists.by_cat, name='cat'),
    path('<kind:kind>', lists.by_kind, name='index'),
    path('<kind:kind>/page/<int:page>', lists.by_kind, name='index'),
    path('<kind:kind>/atom', feeds.AtomByKind(), name='atom_by_kind'),
    path('<kind:kind>/rss', feeds.RssByKind(), name='rss_by_kind'),

    path('<kind:kind>/<int:id>', perma.entry, name='entry'),
    path('<kind:kind>/<int:id>/<slug:slug>', perma.entry, name='entry'),
)


class IndexCrumb(crumbs.Crumb):
    def __init__(self):
        super().__init__(prefix('index'), parent='home:index')

    @property
    def kind(self):
        return self.match.kwargs['kind']

    @property
    def label(self):
        return self.kind.plural

    @property
    def url(self):
        return reverse(prefix('index'), kwargs={'kind': self.kind})


crumbs.add(prefix('cat'), parent='home:index')
crumbs.add(IndexCrumb())
crumbs.add(prefix('entry'), parent=prefix('index'))
