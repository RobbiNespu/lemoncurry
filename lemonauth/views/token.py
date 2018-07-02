from django.views import View
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt

from .. import tokens
from ..models import IndieAuthCode
from lemoncurry import utils


@method_decorator(csrf_exempt, name='dispatch')
class TokenView(View):
    def get(self, req):
        token = tokens.auth(req)
        res = {
            'me': token.me,
            'client_id': token.client_id,
            'scope': token.scope,
        }
        return utils.choose_type(req, res)

    def post(self, req):
        post = req.POST
        try:
            code = IndieAuthCode.objects.get(pk=post.get('code'))
        except IndieAuthCode.DoesNotExist:
            return utils.forbid('invalid auth code')
        code.delete()
        if code.expired:
            return utils.forbid('invalid auth code')

        if code.response_type != 'code':
            return utils.bad_req(
                'this endpoint only supports response_type=code'
            )
        if 'client_id' in post and code.client_id != post['client_id']:
            return utils.forbid('client id did not match')
        if code.redirect_uri != post.get('redirect_uri'):
            return utils.forbid('redirect uri did not match')

        if 'me' in post and code.me != post['me']:
            return utils.forbid('me did not match')

        return utils.choose_type(req, {
            'access_token': tokens.gen_token(code),
            'me': code.me,
            'scope': code.scope,
        })
