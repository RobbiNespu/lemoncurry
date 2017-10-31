from django.contrib.sites.models import Site
from django.contrib.syndication.views import Feed
from django.urls import reverse
from django.utils.feedgenerator import Atom1Feed
from urllib.parse import urljoin
from .models import Entry


class EntriesFeed(Feed):
    def item_title(self, entry):
        return entry.title

    def item_description(self, entry):
        return entry.content

    def item_author_name(self, entry):
        return entry.author.name

    def item_author_email(self, entry):
        return entry.author.email

    def item_author_link(self, entry):
        base = 'https://' + Site.objects.get_current().domain
        return urljoin(base, entry.author.url)

    def item_pubdate(self, entry):
        return entry.published

    def item_updatedate(self, entry):
        return entry.updated


class RssByKind(EntriesFeed):
    def __init__(self, kind):
        self.kind = kind

    def title(self):
        return "{0} ~ {1}".format(
            self.kind.plural,
            Site.objects.get_current().name,
        )

    def link(self):
        return reverse('entries:' + self.kind.index)

    def description(self):
        return "all {0} at {1}".format(
            self.kind.plural,
            Site.objects.get_current().name,
        )

    def items(self):
        return Entry.objects.filter(kind=self.kind.id)


class AtomByKind(RssByKind):
    feed_type = Atom1Feed
    subtitle = RssByKind.description


class RssAllEntries(EntriesFeed):
    def title(self):
        return Site.objects.get_current().name

    def link(self):
        return reverse('home:index')

    def description(self):
        return "content from {0}".format(
            Site.objects.get_current().name,
        )

    def items(self):
        return Entry.objects.all()


class AtomAllEntries(RssAllEntries):
    feed_type = Atom1Feed
    subtitle = RssAllEntries.description
