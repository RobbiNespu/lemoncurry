from django.http import HttpResponseBadRequest, HttpResponseNotFound
from django.http import JsonResponse
from users.models import User
from django.shortcuts import get_object_or_404
from urllib.parse import urlparse, urljoin
from lemoncurry.utils import origin

AVATAR = 'http://webfinger.net/rel/avatar'
PROFILE_PAGE = 'http://webfinger.net/rel/profile-page'


def webfinger(request):
    if 'resource' not in request.GET:
        return HttpResponseBadRequest('resource parameter missing')
    try:
        resource = urlparse(request.GET['resource'])
    except ValueError:
        return HttpResponseBadRequest('resource parameter malformed')

    if resource.scheme in ('mailto', 'acct', 'xmpp'):
        user = get_object_or_404(User, email=resource.path)
    elif resource.scheme in ('http', 'https'):
        user = get_object_or_404(User, pk=1)
    else:
        return HttpResponseNotFound('resource not found on this server')

    base = origin(request)

    def link(rel, href, type):
        return {'rel': rel, 'href': urljoin(base, href), 'type': type}

    info = {
        'subject': 'acct:' + user.email,
        'aliases': (
            urljoin(base, user.url),
            'mailto:' + user.email,
        ),
        'links': (
            link(rel=AVATAR, href=user.avatar.url, type='image/png'),
            link(rel=PROFILE_PAGE, href=user.url, type='text/html'),
        ),
    }
    return JsonResponse(info, content_type='application/jrd+json')
