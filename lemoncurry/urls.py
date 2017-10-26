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
from django.conf import settings
from django.conf.urls import include, url
from django.contrib import admin
from otp_agents.admin import TrustedAgentAdminSite

import django.contrib.sitemaps.views as sitemap
from entries.sitemaps import EntriesSitemap
from home.sitemaps import HomeSitemap

otp_admin_site = TrustedAgentAdminSite()
for model_cls, model_admin in admin.site._registry.items():
    otp_admin_site.register(model_cls, model_admin.__class__)


sections = {
    'entries': EntriesSitemap,
    'home': HomeSitemap,
}
maps = {'sitemaps': sections}

urlpatterns = [
    url('', include('home.urls')),
    url('', include('entries.urls')),
    url('^.well-known/', include('wellknowns.urls')),
    url('^admin/', otp_admin_site.urls),
    url('^auth/', include('lemonauth.urls')),

    url(r'^sitemap\.xml$', sitemap.index, maps),
    url(r'^sitemaps/(?P<section>.+)\.xml$', sitemap.sitemap, maps,
        name='django.contrib.sitemaps.views.sitemap'),
]

if settings.DEBUG:
    import debug_toolbar
    urlpatterns = [
        url(r'^__debug__/', include(debug_toolbar.urls)),
    ] + urlpatterns
