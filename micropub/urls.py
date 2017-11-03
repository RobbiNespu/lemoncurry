from django.conf.urls import url
from . import views

app_name = 'micropub'
urlpatterns = (
    url('^$', views.micropub, name='micropub'),
)
