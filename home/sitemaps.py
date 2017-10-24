from django.contrib import sitemaps
from django.urls import reverse


class HomeSitemap(sitemaps.Sitemap):
    changefreq = 'daily'

    def items(self):
        return ('home:index',)

    def location(self, item):
        return reverse(item)
