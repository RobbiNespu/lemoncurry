import jwt

from datetime import datetime, timedelta
from django.conf import settings


def encode(payload):
    return jwt.encode(payload, settings.SECRET_KEY, algorithm='HS256')


def decode(token):
    return jwt.decode(token, settings.SECRET_KEY, algorithms=('HS256',))


def gen_auth_code(post):
    params = {'me': post['me']}
    if 'state' in post:
        params['state'] = post['state']

    code = {
        'me': post['me'],
        'id': post['client_id'],
        'uri': post['redirect_uri'],
        'typ': post.get('response_type', 'id'),
        'iat': datetime.utcnow(),
        'exp': datetime.utcnow() + timedelta(seconds=30),
    }
    if 'scope' in post:
        code['sco'] = ' '.join(post.getlist('scope'))

    params['code'] = encode(code)
    return params


def verify_auth_code(c):
    return decode(c)
