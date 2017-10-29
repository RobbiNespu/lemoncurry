from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.functional import cached_property
from meta.models import ModelMeta


def avatar_path(instance, name):
    return 'avatars/{id}/{name}'.format(id=instance.id, name=name)


class Site(models.Model):
    name = models.CharField(max_length=100, unique=True)
    icon = models.CharField(max_length=100)
    url = models.CharField(max_length=100)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ('name',)


class User(ModelMeta, AbstractUser):
    avatar = models.ImageField(upload_to=avatar_path)
    note = models.TextField(blank=True)
    # This is gonna need to change if I ever decide to add multiple-user support ;)
    url = '/'

    def get_absolute_url(self):
        return self.url

    @property
    def avatar_url(self):
        return self.avatar.url

    @cached_property
    def facebook_id(self):
        try:
            return self.profiles.filter(site__name='Facebook').values('username')[0]['username']
        except IndexError:
            return None

    @cached_property
    def twitter_username(self):
        try:
            return '@' + self.profiles.filter(site__name='Twitter').values('username')[0]['username']
        except IndexError:
            return None

    _metadata = {
        'image': 'avatar_url',
        'description': 'note',
        'og_type': 'profile',
        'og_profile_id': 'facebook_id',
        'twitter_creator': 'twitter_username',
    }


class ProfileManager(models.Manager):
    def get_queryset(self):
        return super(ProfileManager, self).get_queryset().select_related('site')


class Profile(models.Model):
    objects = ProfileManager()
    user = models.ForeignKey(
        User,
        related_name='profiles',
        on_delete=models.CASCADE
    )
    site = models.ForeignKey(Site, on_delete=models.CASCADE)
    username = models.CharField(max_length=100)
    display_name = models.CharField(max_length=100, blank=True)

    def __str__(self):
        return self.url

    @property
    def name(self):
        return self.display_name or self.username

    @property
    def url(self):
        return self.site.url.format(username=self.username)

    class Meta:
        ordering = ('site', 'username')


class Key(models.Model):
    user = models.ForeignKey(
        User,
        related_name='keys',
        on_delete=models.CASCADE
    )
    fingerprint = models.CharField(max_length=40)
    file = models.FileField(upload_to='keys')

    @property
    def key_id(self): return self.fingerprint[32:]

    def __str__(self):
        return self.key_id

    def pretty_print(self):
        return " ".join(self.fingerprint[i:i+4] for i in range(0, 40, 4))
