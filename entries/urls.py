from django.conf.urls import url
from . import kinds, views
from lemoncurry import breadcrumbs

app_name = 'entries'
urlpatterns = []
for k in kinds.all:
    urlpatterns.append(
        url(r'^{k}$'.format(k=k.plural), views.index, name=k.index, kwargs={'kind': k})
    )
    breadcrumbs.add(app_name + ':' + k.index, label=k.plural, parent='home:index')

    pattern = r'^{k}/(?P<id>\d+)'.format(k=k.plural)
    urlpatterns.append(
        url(pattern + '$', views.entry, name=k.entry)
    )
    breadcrumbs.add(app_name + ':' + k.entry, parent=app_name + ':' + k.index)
    if k.has('slug'):
        urlpatterns.append(
            url(pattern + r'/(?P<slug>.+)$', views.entry, name=k.entry_slug)
        )
        breadcrumbs.add(app_name + ':' + k.entry_slug, parent=app_name + ':' + k.index)
