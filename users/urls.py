from django.urls import re_path

from .views import libravatar

app_name = 'users'
urlpatterns = (
    re_path('^avatar/(?P<hash>[a-z0-9]+)$', libravatar, name='libravatar'),
)
