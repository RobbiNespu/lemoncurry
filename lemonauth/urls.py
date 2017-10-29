from django.conf.urls import url
from . import views

app_name = 'lemonauth'
urlpatterns = [
    url('^login$', views.login, name='login'),
    url('^logout$', views.logout, name='logout'),
    url('^indie$', views.IndieView.as_view(), name='indie'),
    url('^indie/approve$', views.indie_approve, name='indie_approve'),
]
