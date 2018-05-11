from django.http import HttpResponseBadRequest, HttpResponseRedirect
from urllib.parse import urlencode, urlparse

from users.models import User

AVATAR = 'http://webfinger.net/rel/avatar'
PROFILE_PAGE = 'http://webfinger.net/rel/profile-page'
BRIDGY_FED = 'https://fed.brid.gy/.well-known/webfinger'


def https_resource_matching(resource):
    """
    Takes a `urllib.parse.urlparse` tuple representing a WebFinger resource and
    translates ``mailto:`` and ``xmpp:`` resources to an equivalent ``https:``
    resource, if a user with matching email or XMPP address exists locally.
    Will throw `User.DoesNotExist` if no such user exists.
    """
    if resource.scheme == 'mailto':
        query = {'email': resource.path}
    else:
        query = {'xmpp': resource.path}
    return User.objects.get(**query).absolute_url


def webfinger(request):
    """
    A thin wrapper around Bridgy Fed's implementation of WebFinger.

    In most cases, this view simply redirects to the same endpoint at Bridgy.
    However, Bridgy does not support the ``mailto:`` and ``xmpp:`` resource
    schemes - quite reasonably, since there's no possible way to discover the
    ``acct:`` they go with! - so resources with those schemes are translated
    locally into an ``https:`` URL representing the same person, and *then*
    redirected to Bridgy.

    Additionally, WebFinger requests with a missing or malformed resource will
    be rejected immediately rather than passed on to Bridgy.

    Note that the translation step will only be applied if there exists a
    :model:`users.User` with matching email or XMPP address. Otherwise, the
    original resource will be preserved in the redirect - and likely fail to
    find anything at Bridgy's end either.
    """
    if 'resource' not in request.GET:
        return HttpResponseBadRequest('resource parameter missing')
    resource = request.GET['resource']
    try:
        res = urlparse(resource)
    except ValueError:
        return HttpResponseBadRequest('resource parameter malformed')

    if res.scheme in ('mailto', 'xmpp'):
        try:
            resource = https_resource_matching(res)
        except User.DoesNotExist:
            pass

    query = urlencode({'resource': resource})
    return HttpResponseRedirect(BRIDGY_FED + '?' + query)
