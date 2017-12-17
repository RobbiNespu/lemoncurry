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
        token = tokens.auth(req)
        if hasattr(token, 'content'):
            return token
        res = {
            'me': token.me,
            'client_id': token.client,
            'scope': token.scope,
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
