from django.conf import settings
from django.urls import path

from .views import unshort

app_name = 'lemonshort'
urlpatterns = tuple(
    path('{0!s}<tiny>'.format(k), unshort, name=m, kwargs={'model': m})
    for k, m in settings.SHORTEN_MODELS.items()
)
