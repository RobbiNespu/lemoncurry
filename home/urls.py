from django.urls import path

from . import views

app_name = 'home'
urlpatterns = [
    path('', views.index, name='index'),
    path('page/<int:page>', views.index, name='index'),
    path('robots.txt', views.robots, name='robots.txt'),
]
