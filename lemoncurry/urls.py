"""lemoncurry URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from typing import Tuple

from django.conf import settings
from django.urls import include, path
from django.urls.resolvers import URLPattern
from django.views.generic import RedirectView

from django.contrib import admin
import django.contrib.sitemaps.views as sitemap

from entries.sitemaps import EntriesSitemap
from home.sitemaps import HomeSitemap

sections = {
    'entries': EntriesSitemap,
    'home': HomeSitemap,
}
maps = {'sitemaps': sections}

urlpatterns = (
    path('', include('home.urls')),
    path('', include('entries.urls')),
    path('', include('users.urls')),
    path('.well-known/', include('wellknowns.urls')),
    path('admin/doc/', include('django.contrib.admindocs.urls')),
    path('admin/', admin.site.urls),
    path('auth/', include('lemonauth.urls')),
    path('favicon.ico', RedirectView.as_view(
        url=settings.MEDIA_URL + 'favicon/favicon.ico')),
    path('micropub', include('micropub.urls')),
    path('s/', include('lemonshort.urls')),
    path('webmention', include('webmention.urls')),

    path('django-rq/', include('django_rq.urls')),
    path('sitemap.xml', sitemap.index, maps, name='sitemap'),
    path('sitemaps/<section>.xml', sitemap.sitemap, maps,
         name='django.contrib.sitemaps.views.sitemap'),
)  # type: Tuple[URLPattern, ...]

if settings.DEBUG:
    import debug_toolbar
    urlpatterns += (
        path('__debug__/', include(debug_toolbar.urls)),
    )
