from django.db import models
from django.contrib.auth.models import AbstractUser


def avatar_path(instance, name):
    return 'avatars/{id}/{name}'.format(id=instance.id, name=name)


class User(AbstractUser):
    avatar = models.ImageField(upload_to=avatar_path)
    note = models.TextField(blank=True)
