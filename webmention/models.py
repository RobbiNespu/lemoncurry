from django.db import models
from entries.models import Entry
from model_utils.models import TimeStampedModel


class State:
    PENDING = 'p'
    VALID = 'v'
    INVALID = 'i'
    DELETED = 'd'
    CHOICES = (
        (PENDING, 'pending'),
        (VALID, 'valid'),
        (INVALID, 'invalid'),
        (DELETED, 'deleted'),
    )


class Webmention(TimeStampedModel):
    entry = models.ForeignKey(Entry, on_delete=models.CASCADE)
    source = models.CharField(max_length=255)
    target = models.CharField(max_length=255)
    state = models.CharField(
        choices=State.CHOICES,
        default=State.PENDING,
        max_length=1
    )

    class Meta:
        default_related_name = 'mentions'
        unique_together = ('source', 'target')
