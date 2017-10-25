from django.contrib import sitemaps
from .models import Entry


class EntriesSitemap(sitemaps.Sitemap):
    def items(self):
        return Entry.objects.all()

    def lastmod(self, entry):
        return entry.updated
    
    def location(self, entry):
        return entry.url
