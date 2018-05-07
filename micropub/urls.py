from django.urls import path
from .views import micropub
from .views.media import media

app_name = 'micropub'
urlpatterns = (
    path('', micropub, name='micropub'),
    path('/media', media, name='media'),
)
