from django.conf import settings
from django.contrib.sites.models import Site
from django.contrib.syndication.views import Feed
from django.urls import reverse
from django.utils.feedgenerator import Atom1Feed
from lemoncurry.templatetags.markdown import markdown
from ..kinds import on_home
from ..models import Entry


class Atom1FeedWithHub(Atom1Feed):
    def add_root_elements(self, handler):
        super().add_root_elements(handler)
        handler.startElement('link', {'rel': 'hub', 'href': settings.PUSH_HUB})
        handler.endElement('link')


class EntriesFeed(Feed):
    item_guid_is_permalink = True

    def item_link(self, entry):
        return entry.absolute_url

    def item_title(self, entry):
        return entry.title

    def item_description(self, entry):
        return markdown(entry.content)

    def item_author_name(self, entry):
        return entry.author.name

    def item_author_email(self, entry):
        return entry.author.email

    def item_author_link(self, entry):
        return entry.author.absolute_url

    def item_pubdate(self, entry):
        return entry.published

    def item_updateddate(self, entry):
        return entry.updated

    def item_categories(self, entry):
        return (cat.name for cat in entry.cats.all())


class RssByKind(EntriesFeed):
    def get_object(self, request, kind):
        return kind

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
    feed_type = Atom1FeedWithHub
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
    feed_type = Atom1FeedWithHub
    subtitle = RssHomeEntries.description
