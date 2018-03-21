from django.conf import settings
from django.conf.urls import url

from .views import unshort

app_name = 'lemonshort'
urlpatterns = tuple(
    url(r'^{0!s}(?P<tiny>\w+)$'.format(k), unshort, kwargs={'model': m})
    for k, m in settings.SHORTEN_MODELS.items()
)
