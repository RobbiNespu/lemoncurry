from django.contrib.sites.models import Site
from django.contrib.syndication.views import Feed
from django.urls import reverse
from django.utils.feedgenerator import Atom1Feed
from urllib.parse import urljoin
from lemoncurry.templatetags.markdown import markdown
from ..kinds import from_plural, on_home
from ..models import Entry


class EntriesFeed(Feed):
    def item_title(self, entry):
        return entry.title

    def item_description(self, entry):
        return markdown(entry.content)

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

    def item_categories(self, entry):
        return (cat.name for cat in entry.cats.all())


class RssByKind(EntriesFeed):
    def get_object(self, request, kind):
        return from_plural[kind]

    def title(self, kind):
        return "{0} ~ {1}".format(
            kind.plural,
            Site.objects.get_current().name,
        )

    def link(self, kind):
        return kind.index

    def description(self, kind):
        return "all {0} at {1}".format(
            kind.plural,
            Site.objects.get_current().name,
        )

    def items(self, kind):
        return Entry.objects.filter(kind=kind.id)


class AtomByKind(RssByKind):
    feed_type = Atom1Feed
    subtitle = RssByKind.description


class RssHomeEntries(EntriesFeed):
    def title(self):
        return Site.objects.get_current().name

    def link(self):
        return reverse('home:index')

    def description(self):
        return "content from {0}".format(
            Site.objects.get_current().name,
        )

    def items(self):
        return Entry.objects.filter(kind__in=on_home)


class AtomHomeEntries(RssHomeEntries):
    feed_type = Atom1Feed
    subtitle = RssHomeEntries.description
