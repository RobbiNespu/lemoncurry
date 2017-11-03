from django.contrib.auth import get_user_model
from django.views import View
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from urllib.parse import urljoin

from .. import tokens
from lemoncurry import utils


@method_decorator(csrf_exempt, name='dispatch')
class TokenView(View):
    def get(self, req):
        token = req.META.get('HTTP_AUTHORIZATION', '').split(' ')
        if not token:
            return utils.bad_req('missing Authorization header')
        if token[0] != 'Bearer':
            return utils.bad_req('only Bearer auth is supported')
        try:
            token = tokens.decode(token[1])
        except Exception:
            return utils.forbid('invalid token')

        user = get_user_model().objects.get(pk=token['uid'])
        me = urljoin(utils.origin(req), user.url)
        res = {
            'me': me,
            'client_id': token['cid'],
            'scope': token['sco'],
        }
        return utils.choose_type(req, res)

    def post(self, req):
        post = req.POST
        try:
            code = tokens.decode(post.get('code'))
        except Exception:
            return utils.forbid('invalid auth code')

        if code['typ'] != 'code':
            return utils.bad_req(
                'this endpoint only supports response_type=code'
            )
        if code['cid'] != post.get('client_id'):
            return utils.forbid('client id did not match')
        if code['uri'] != post.get('redirect_uri'):
            return utils.forbid('redirect uri did not match')

        user = get_user_model().objects.get(pk=code['uid'])
        me = urljoin(utils.origin(req), user.url)
        if me != post.get('me'):
            return utils.forbid('me did not match')

        return utils.choose_type(req, {
            'access_token': tokens.gen_token(code),
            'me': me,
            'scope': code['sco'],
        })
