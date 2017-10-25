from django.conf.urls import url
from . import kinds, views
from lemoncurry import breadcrumbs

app_name = 'entries'
urlpatterns = []
for k in kinds.all:
    index = k.plural + '_index'
    urlpatterns.append(
        url(r'^{k}$'.format(k=k.plural), views.index, name=index, kwargs={'kind': k})
    )
    breadcrumbs.add(app_name + ':' + index, label=k.plural, parent='home:index')

    entry = k.plural + '_entry'
    pattern = r'^{k}/(?P<id>\d+)'.format(k=k.plural)
    urlpatterns.append(
        url(pattern + '$', views.entry, name=entry)
    )
    breadcrumbs.add(app_name + ':' + entry, parent=app_name + ':' + index)
    if k.has('slug'):
        urlpatterns.append(
            url(pattern + r'/(?P<slug>.+)$', views.entry, name=entry + '_slug')
        )
        breadcrumbs.add(app_name + ':' + entry + '_slug', parent=app_name + ':' + index)
