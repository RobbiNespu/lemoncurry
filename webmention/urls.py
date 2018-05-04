from django.urls import path
from . import views

app_name = 'webmention'
urlpatterns = (
    path('', views.accept, name='accept'),
    path('s/<int:mention_id>', views.status, name='status')
)
