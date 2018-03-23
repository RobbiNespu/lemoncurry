from django.conf.urls import url

from .views import libravatar

app_name = 'users'
urlpatterns = (
    url('^avatar/(?P<hash>[a-z0-9]+)$', libravatar, name='libravatar'),
)
