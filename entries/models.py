from django.contrib.auth import get_user_model
from django.db import models

from . import kinds
ENTRY_KINDS = [(k.id, k.__name__) for k in kinds.all]


class Entry(models.Model):
    kind = models.CharField(
        max_length=30,
        choices=ENTRY_KINDS,
        default=ENTRY_KINDS[0][0]
    )

    name = models.CharField(max_length=100, blank=True)
    summary = models.TextField(blank=True)
    content = models.TextField()

    author = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)

    published = models.DateTimeField()
    updated = models.DateTimeField()

    def __str__(self):
        return '{kind} {id}: {content}'.format(
            kind=self.kind,
            id=self.id,
            content=self.content
        )

    class Meta:
        verbose_name_plural = 'entries'
        ordering = ['-published']
