from django.urls import path

from . import views

app_name = 'wellknowns'
urlpatterns = [
    path('keybase.txt', views.keybase, name='keybase'),
    path('host-meta', views.host_meta_xml, name='host-meta'),
    path('host-meta.json', views.host_meta_json, name='host-meta.json'),
    path('manifest.json', views.manifest, name='manifest'),
    path('webfinger', views.webfinger, name='webfinger'),
]
