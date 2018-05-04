from computed_property import ComputedCharField
from django.db import models
from django.contrib.auth.models import AbstractUser, UserManager as DjangoUserManager
from django.contrib.sites.models import Site as DjangoSite
from django.utils.functional import cached_property
from hashlib import md5, sha256
from meta.models import ModelMeta
from urllib.parse import urljoin
from lemoncurry import utils


def avatar_path(instance, name):
    return 'avatars/{id}/{name}'.format(id=instance.id, name=name)


class Site(models.Model):
    name = models.CharField(max_length=100, unique=True)
    icon = models.CharField(max_length=100)
    domain = models.CharField(max_length=100, blank=True)
    url_template = models.CharField(max_length=100)

    def format(self, username=''):
        return self.url_template.format(domain=self.domain, username=username)

    @property
    def url(self):
        return self.format()

    def __str__(self):
        return self.name

    class Meta:
        ordering = ('name',)


class UserManager(DjangoUserManager):
    def get_queryset(self):
        return super(UserManager, self).get_queryset().prefetch_related('keys', 'profiles')


class User(ModelMeta, AbstractUser):
    """
    A user in the system - each user will have a representative h-card
    generated based on all their associated information and may author as many
    h-entries (:model:`entries.Entry`) as they wish.
    """
    objects = UserManager()

    avatar = models.ImageField(
        upload_to=avatar_path,
        help_text='an avatar or photo that represents this user'
    )
    note = models.TextField(
        blank=True,
        help_text='a bio or short description provided by the user'
    )
    xmpp = models.EmailField(
        blank=True,
        help_text='an XMPP address through which the user may be reached'
    )

    # This is gonna need to change if I ever decide to add multiple-user support ;)
    url = '/'

    email_md5 = ComputedCharField(
        compute_from='calc_email_md5', max_length=32, unique=True,
        help_text="MD5 hash of the user's email, used for Libravatar"
    )
    email_sha256 = ComputedCharField(
        compute_from='calc_email_sha256', max_length=64, unique=True,
        help_text="SHA-256 hash of the user's email, used for Libravatar"
    )

    @property
    def calc_email_md5(self):
        return md5(self.email.lower().encode('utf-8')).hexdigest()

    @property
    def calc_email_sha256(self):
        return sha256(self.email.lower().encode('utf-8')).hexdigest()

    @property
    def name(self):
        return '{0} {1}'.format(self.first_name, self.last_name)

    def get_absolute_url(self):
        return self.url

    @property
    def full_url(self):
        base = 'https://' + DjangoSite.objects.get_current().domain
        return urljoin(base, self.url)

    @property
    def description(self):
        return utils.to_plain(self.note)

    @property
    def avatar_url(self):
        return self.avatar.url

    @cached_property
    def facebook_id(self):
        for p in self.profiles.all():
            if p.site.name == 'Facebook':
                return p.username
        return None

    @cached_property
    def twitter_username(self):
        for p in self.profiles.all():
            if p.site.name == 'Twitter':
                return '@' + p.username
        return None

    @property
    def json_ld(self):
        base = 'https://' + DjangoSite.objects.get_current().domain
        return {
            '@context': 'http://schema.org',
            '@type': 'Person',
            '@id': self.full_url,
            'url': self.full_url,
            'name': self.name,
            'email': self.email,
            'image': urljoin(base, self.avatar.url),
            'givenName': self.first_name,
            'familyName': self.last_name,
            'sameAs': [profile.url for profile in self.profiles.all()]
        }

    _metadata = {
        'image': 'avatar_url',
        'description': 'description',
        'og_type': 'profile',
        'og_profile_id': 'facebook_id',
        'twitter_creator': 'twitter_username',
    }


class ProfileManager(models.Manager):
    def get_queryset(self):
        return super(ProfileManager, self).get_queryset().select_related('site')


class Profile(models.Model):
    """
    Represents a particular :model:`users.User`'s identity on a particular
    :model:`users.Site` - each user may have as many profiles on as many sites
    as they wish, and all profiles will become `rel="me"` links on their
    representative h-card. Additionally, :model:`entries.Syndication` is
    tracked by linking each syndication to a particular profile.
    """
    objects = ProfileManager()
    user = models.ForeignKey(
        User,
        related_name='profiles',
        on_delete=models.CASCADE
    )
    site = models.ForeignKey(Site, on_delete=models.CASCADE)
    username = models.CharField(
        max_length=100,
        help_text="the user's actual handle or ID on the remote site"
    )
    display_name = models.CharField(
        max_length=100,
        blank=True,
        help_text="overrides the username for display - useful for sites that use ugly IDs"
    )

    def __str__(self):
        if self.site.domain:
            return self.name + '@' + self.site.domain
        return self.name

    @property
    def name(self):
        return self.display_name or self.username

    @property
    def url(self):
        return self.site.format(username=self.username)

    class Meta:
        ordering = ('site', 'username')


class Key(models.Model):
    """
    Represents a PGP key that belongs to a particular :model:`users.User`. Each
    key will be added to the user's h-card with rel="pgpkey", a format
    compatible with IndieAuth.com.
    """
    user = models.ForeignKey(
        User,
        related_name='keys',
        on_delete=models.CASCADE
    )
    fingerprint = models.CharField(max_length=40)
    file = models.FileField(upload_to='keys')

    @property
    def key_id(self):
        """
        Returns the key ID, defined as the last eight characters of the key's
        fingerprint. Key IDs are not cryptographically secure (it's easy to
        forge a key with any key ID of your choosing), but when you have
        already imported a key using its full fingerprint, the key ID is a
        convenient way to refer to it.
        """
        return self.fingerprint[32:]

    def __str__(self):
        return self.key_id

    def pretty_print(self):
        """
        Groups the PGP fingerprint into four-character chunks for display, the
        same way GnuPG does. This can make reading the fingerprint a little
        friendlier.
        """
        return " ".join(self.fingerprint[i:i+4] for i in range(0, 40, 4))
