import jwt

from datetime import datetime, timedelta
from django.conf import settings


def gen_auth_code(post):
    params = {'me': post['me']}
    if 'state' in post:
        params['state'] = post['state']

    code = {
        'me': post['me'],
        'client_id': post['client_id'],
        'redirect_uri': post['redirect_uri'],
        'response_type': post.get('response_type', 'id'),
        'exp': datetime.utcnow() + timedelta(minutes=10),
    }
    if 'scope' in post:
        code['scope'] = ' '.join(post.getlist('scope'))

    params['code'] = jwt.encode(code, settings.SECRET_KEY)
    return params


def verify_auth_code(c):
    return jwt.decode(c, settings.SECRET_KEY)
