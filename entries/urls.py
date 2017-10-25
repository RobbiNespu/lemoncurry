from django.conf.urls import url
from . import kinds, views
from lemoncurry import breadcrumbs

app_name = 'entries'
urlpatterns = []
for k in kinds.all:
    index = k.plural + '_index'
    urlpatterns.extend((
        url(k.plural, views.index, name=index, kwargs={'kind': k}),
    ))
    breadcrumbs.add(app_name + ':' + index, label=k.plural, parent='home:index')
