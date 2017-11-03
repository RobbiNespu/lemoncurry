from jose import jwt

from datetime import datetime, timedelta
from django.conf import settings


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
