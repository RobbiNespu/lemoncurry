from django.conf.urls import url
from . import kinds
from .views import feeds, lists, perma
from lemoncurry import breadcrumbs as crumbs


def to_pat(*args):
    return '^{0}$'.format(''.join(args))


def prefix(route):
    return app_name + ':' + route


page = '(?:/page/(?P<page>\d+))?'
slug = r'/(?P<slug>[^/]+)'

app_name = 'entries'
urlpatterns = [
    url('^atom$', feeds.AtomHomeEntries(), name='atom'),
    url('^rss$', feeds.RssHomeEntries(), name='rss'),
    url(to_pat('cats', slug, page), lists.by_cat, name='cat'),
]
crumbs.add(prefix('cat'), parent='home:index')

slug = '(?:' + slug + ')?'

for k in kinds.all:
    kind = k.plural
    id = r'/(?P<id>\d+)'
    urlpatterns += (
        url(to_pat(kind, page), lists.by_kind, name=k.index, kwargs={'kind': k}),
        url(to_pat(kind, '/atom'), feeds.AtomByKind(k), name=k.atom),
        url(to_pat(kind, '/rss'), feeds.RssByKind(k), name=k.rss),
        url(to_pat(kind, id, slug, '/amp'), perma.entry_amp, name=k.entry_amp),
        url(to_pat(kind, id, slug), perma.entry, name=k.entry),
    )

    crumbs.add(prefix(k.index), label=k.plural, parent='home:index')
    crumbs.add(prefix(k.entry), parent=prefix(k.index))
