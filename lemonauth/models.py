from django.db import models
from secrets import token_hex


class IndieAuthCodeManager(models.Manager):
    def create_from_qdict(self, d):
        code = self.create(
            me=d['me'],
            client_id=d['client_id'],
            redirect_uri=d['redirect_uri'],
            response_type=d.get('response_type', 'id'),
            scope=" ".join(d.getlist('scope')),
        )
        code.code = token_hex(32)
        return code


class IndieAuthCode(models.Model):
    objects = IndieAuthCodeManager()
    code = models.CharField(max_length=64, unique=True)
    me = models.CharField(max_length=255)
    client_id = models.CharField(max_length=255)
    redirect_uri = models.CharField(max_length=255)
    response_type = models.CharField(
        max_length=4,
        choices=(('id', 'id'), ('code', 'code')),
        default='id',
    )
    scope = models.CharField(max_length=200, blank=True)
