from django.conf.urls import url
from . import kinds, views
from lemoncurry import breadcrumbs as crumbs


def to_pat(*args):
    return '^{0}$'.format(''.join(args))


def prefix(route):
    return app_name + ':' + route


app_name = 'entries'
urlpatterns = []
for k in kinds.all:
    kind = k.plural
    id = r'/(?P<id>\d+)'
    slug = r'(?:/(?P<slug>.+))?'
    urlpatterns += (
        url(to_pat(kind), views.index, name=k.index, kwargs={'kind': k}),
        url(to_pat(kind, id, slug), views.entry, name=k.entry),
    )

    crumbs.add(prefix(k.index), label=k.plural, parent='home:index')
    crumbs.add(prefix(k.entry), parent=prefix(k.index))
