from django.urls import path
from . import views

app_name = 'lemonauth'
urlpatterns = [
    path('login', views.login, name='login'),
    path('logout', views.logout, name='logout'),
    path('indie', views.IndieView.as_view(), name='indie'),
    path('indie/approve', views.indie_approve, name='indie_approve'),
    path('token', views.TokenView.as_view(), name='token'),
]
