from datetime import timedelta
from django.contrib.auth import get_user_model
from django.db import models
from django.utils.timezone import now
from randomslugfield import RandomSlugField
from model_utils import Choices
from model_utils.fields import StatusField
from model_utils.models import TimeStampedModel


class AuthSecret(TimeStampedModel):
    """
    An AuthSecret is a model with an unguessable primary key, suitable for
    sharing with external sites for secure authentication.

    AuthSecret is primarily used to factor out the many similarities between
    authorisation codes and tokens in IndieAuth - the two contain many
    identical fields, but just a few differences.
    """
    id = RandomSlugField(primary_key=True, length=30)
    client_id = models.URLField()
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    scope = models.TextField(blank=True)

    @property
    def me(self):
        return self.user.full_url

    def __contains__(self, scope):
        return scope in self.scope.split(' ')

    class Meta:
        abstract = True


class IndieAuthCode(AuthSecret):
    """
    An IndieAuthCode is an authorisation code that a client must provide to us
    to complete the IndieAuth process.

    Codes are single-use, and if unused will be expired automatically after
    thirty seconds.
    """
    redirect_uri = models.URLField()

    RESPONSE_TYPE = Choices('id', 'code')
    response_type = StatusField(choices_name='RESPONSE_TYPE')

    @property
    def expired(self):
        return self.created + timedelta(seconds=30) < now()


class Token(AuthSecret):
    """
    A Token grants a client long-term authorisation - it will not expire unless
    explicitly revoked by the user.
    """
    pass
