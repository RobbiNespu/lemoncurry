from django.conf.urls import url

from . import views

app_name = 'wellknowns'
urlpatterns = [
    url(r'^keybase.txt$', views.keybase, name='keybase'),
    url(r'^host-meta$', views.host_meta_xml, name='host-meta'),
    url(r'^host-meta.json$', views.host_meta_json, name='host-meta.json'),
    url(r'^manifest.json$', views.manifest, name='manifest'),
    url(r'^webfinger$', views.webfinger, name='webfinger'),
]
