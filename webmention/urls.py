from django.conf.urls import url
from . import views

app_name = 'webmention'
urlpatterns = (
    url('^$', views.accept, name='accept'),
    url('^s/(?P<id>\d+)$', views.status, name='status')
)
