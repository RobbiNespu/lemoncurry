from django.urls import path
from . import views

app_name = 'micropub'
urlpatterns = (
    path('', views.micropub, name='micropub'),
)
