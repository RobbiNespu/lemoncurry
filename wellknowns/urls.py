from django.conf.urls import url

from . import views

app_name = 'wellknowns'
urlpatterns = [
    url(r'^keybase.txt$', views.keybase, name='keybase'),
]
