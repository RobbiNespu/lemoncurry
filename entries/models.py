from django.contrib.auth import get_user_model
from django.contrib.sites.models import Site
from django.db import models
from django.urls import reverse
from itertools import groupby
from slugify import slugify
from textwrap import shorten
from urllib.parse import urljoin

from meta.models import ModelMeta
from users.models import Profile

from . import kinds
ENTRY_KINDS = [(k.id, k.id) for k in kinds.all]


class EntryManager(models.Manager):
    def get_queryset(self):
        qs = super(EntryManager, self).get_queryset()
        return qs.select_related('author').prefetch_related('syndications')


class Entry(ModelMeta, models.Model):
    objects = EntryManager()
    kind = models.CharField(
        max_length=30,
        choices=ENTRY_KINDS,
        db_index=True,
        default=ENTRY_KINDS[0][0]
    )

    name = models.CharField(max_length=100, blank=True)
    photo = models.ImageField(blank=True)
    content = models.TextField()

    author = models.ForeignKey(
        get_user_model(),
        related_name='entries',
        on_delete=models.CASCADE,
    )

    published = models.DateTimeField()
    updated = models.DateTimeField()

    _metadata = {
        'description': 'excerpt',
        'image': 'image_url',
        'twitter_creator': 'twitter_creator',
        'og_profile_id': 'og_profile_id',
    }

    @property
    def title(self):
        if self.name:
            return self.name
        return shorten(self.paragraphs[0], width=100, placeholder='…')

    @property
    def excerpt(self):
        try:
            return self.paragraphs[0 if self.name else 1]
        except IndexError:
            return ' '

    @property
    def paragraphs(self):
        lines = self.content.splitlines()
        return [
            "\n".join(para) for k, para in groupby(lines, key=bool) if k
        ]

    @property
    def twitter_creator(self):
        return self.author.twitter_username

    @property
    def og_profile_id(self):
        return self.author.facebook_id

    @property
    def image_url(self):
        return self.photo.url if self.photo else self.author.avatar_url

    def __str__(self):
        return '{0} {1}: {2}'.format(self.kind, self.id, self.title)

    def get_absolute_url(self):
        return self.url

    @property
    def url(self):
        kind = kinds.from_id[self.kind]
        args = [self.id]
        if kind.slug:
            args.append(self.slug)
        return reverse('entries:' + kind.entry, args=args)

    @property
    def slug(self):
        return slugify(self.name)

    @property
    def json_ld(self):
        base = 'https://' + Site.objects.get_current().domain
        url = urljoin(base, self.url)

        posting = {
            '@context': 'http://schema.org',
            '@type': 'BlogPosting',
            '@id': url,
            'url': url,
            'mainEntityOfPage': url,
            'author': {
                '@type': 'Person',
                'url': urljoin(base, self.author.url),
                'name': self.author.name,
            },
            'headline': self.title,
            'description': self.excerpt,
            'datePublished': self.published.isoformat(),
            'dateModified': self.updated.isoformat(),
        }
        if self.photo:
            posting['image'] = (urljoin(base, self.photo.url), )
        return posting

    class Meta:
        verbose_name_plural = 'entries'
        ordering = ['-published']


class SyndicationManager(models.Manager):
    def get_queryset(self):
        qs = super(SyndicationManager, self).get_queryset()
        return qs.select_related('profile__site')


class Syndication(models.Model):
    objects = SyndicationManager()
    entry = models.ForeignKey(
        Entry,
        related_name='syndications',
        on_delete=models.CASCADE
    )
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE)
    url = models.CharField(max_length=255)

    class Meta:
        ordering = ['profile']
