from django.db import models
from django.contrib.auth.models import AbstractUser


def avatar_path(instance, name):
    return 'avatars/{id}/{name}'.format(id=instance.id, name=name)


class User(AbstractUser):
    avatar = models.ImageField(upload_to=avatar_path)
    note = models.TextField(blank=True)


class Key(models.Model):
    user = models.ForeignKey(
        User,
        related_name='keys',
        on_delete=models.CASCADE
    )
    fingerprint = models.CharField(max_length=40)
    file = models.FileField(upload_to='keys')

    def pretty_print(self):
        return " ".join(self.fingerprint[i:i+4] for i in range(0, 40, 4))
