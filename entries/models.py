from django.contrib.auth import get_user_model
from django.contrib.sites.models import Site
from django.db import models
from django.urls import reverse
from itertools import groupby
from mf2util import interpret
from slugify import slugify
from textwrap import shorten
from urllib.parse import urljoin

from meta.models import ModelMeta
from model_utils.models import TimeStampedModel
from users.models import Profile

from . import kinds
from lemoncurry import requests, utils
ENTRY_KINDS = [(k.id, k.id) for k in kinds.all]


class CatManager(models.Manager):
    def from_name(self, name):
        cat, created = self.get_or_create(name=name, slug=slugify(name))
        return cat


class Cat(models.Model):
    objects = CatManager()
    name = models.CharField(max_length=255, unique=True)
    slug = models.CharField(max_length=255, unique=True)

    def __str__(self):
        return '#' + self.name

    @property
    def url(self):
        return reverse('entries:cat', args=(self.slug,))

    class Meta:
        ordering = ('name',)


class EntryManager(models.Manager):
    def get_queryset(self):
        qs = super(EntryManager, self).get_queryset()
        return qs.select_related('author').prefetch_related('syndications')


class Entry(ModelMeta, TimeStampedModel):
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

    cats = models.ManyToManyField(Cat, related_name='entries')

    in_reply_to = models.CharField(max_length=255, blank=True)
    like_of = models.CharField(max_length=255, blank=True)
    repost_of = models.CharField(max_length=255, blank=True)

    author = models.ForeignKey(
        get_user_model(),
        related_name='entries',
        on_delete=models.CASCADE,
    )

    @property
    def reply_context(self):
        if not self.in_reply_to:
            return None
        return interpret(
            requests.mf2(self.in_reply_to).to_dict(),
            self.in_reply_to
        )

    @property
    def published(self):
        return self.created

    @property
    def updated(self):
        return self.modified

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
        return shorten(utils.to_plain(self.paragraphs[0]), width=100, placeholder='…')

    @property
    def excerpt(self):
        try:
            return utils.to_plain(self.paragraphs[0 if self.name else 1])
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
    def amp_url(self):
        kind = kinds.from_id[self.kind]
        args = [self.id]
        if kind.slug:
            args.append(self.slug)
        return reverse('entries:' + kind.entry_amp, args=args)

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
            'datePublished': self.created.isoformat(),
            'dateModified': self.modified.isoformat(),
        }
        if self.photo:
            posting['image'] = (urljoin(base, self.photo.url), )
        return posting

    class Meta:
        verbose_name_plural = 'entries'
        ordering = ['-created']


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
