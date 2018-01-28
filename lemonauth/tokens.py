from jose import jwt

from datetime import datetime, timedelta
from django.contrib.auth import get_user_model
from django.conf import settings

from micropub.views import error


def auth(request):
    if 'HTTP_AUTHORIZATION' in request.META:
        auth = request.META.get('HTTP_AUTHORIZATION').split(' ')
        if auth[0] != 'Bearer':
            return error.bad_req('auth type {0} not supported'.format(auth[0]))
        if len(auth) != 2:
            return error.bad_req(
                'invalid Bearer auth format, must be Bearer <token>'
            )
        token = auth[1]
    elif 'access_token' in request.POST:
        token = request.POST.get('access_token')
    elif 'access_token' in request.GET:
        token = request.GET.get('access_token')
    else:
        return error.unauthorized()

    try:
        token = decode(token)
    except Exception as e:
        return error.forbidden()

    return MicropubToken(token)


class MicropubToken:
    def __init__(self, tok):
        self.user = get_user_model().objects.get(pk=tok['uid'])
        self.client = tok['cid']
        self.scope = tok['sco']

        self.me = self.user.full_url
        self.scopes = self.scope.split(' ')

    def __contains__(self, scope):
        return scope in self.scopes


def encode(payload):
    return jwt.encode(payload, settings.SECRET_KEY, algorithm='HS256')


def decode(token):
    return jwt.decode(token, settings.SECRET_KEY, algorithms=('HS256',))


def gen_auth_code(req):
    code = {
        'uid': req.user.id,
        'cid': req.POST['client_id'],
        'uri': req.POST['redirect_uri'],
        'typ': req.POST.get('response_type', 'id'),
        'iat': datetime.utcnow(),
        'exp': datetime.utcnow() + timedelta(seconds=30),
    }
    if 'scope' in req.POST:
        code['sco'] = ' '.join(req.POST.getlist('scope'))

    return encode(code)


def gen_token(code):
    tok = {
        'uid': code['uid'],
        'cid': code['cid'],
        'sco': code['sco'],
        'iat': datetime.utcnow(),
    }
    return encode(tok)
