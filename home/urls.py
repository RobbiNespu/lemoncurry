from django.conf.urls import url

from . import views

app_name = 'home'
urlpatterns = [
    url(r'^(?:page/(?P<page>\d+))?$', views.index, name='index'),
    url(r'^robots.txt$', views.robots, name='robots.txt'),
]
