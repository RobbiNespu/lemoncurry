from annoying.decorators import render_to
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.shortcuts import redirect
from django.utils.decorators import method_decorator
from django.views.generic import TemplateView
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
from lemoncurry import breadcrumbs, requests, utils
from urllib.parse import urlencode, urljoin, urlunparse, urlparse

from .. import tokens
from ..models import IndieAuthCode

breadcrumbs.add('lemonauth:indie', parent='home:index')


def canonical(url):
    if '//' not in url:
        url = '//' + url
    (scheme, netloc, path, params, query, fragment) = urlparse(url)
    if not scheme or scheme == 'http':
        scheme = 'https'
    if not path:
        path = '/'
    return urlunparse((scheme, netloc, path, params, query, fragment))


@method_decorator(csrf_exempt, name='dispatch')
class IndieView(TemplateView):
    template_name = 'lemonauth/indie.html'
    required_params = ('client_id', 'redirect_uri')

    @method_decorator(login_required)
    @method_decorator(render_to(template_name))
    def get(self, request):
        params = request.GET.dict()
        params.setdefault('response_type', 'id')

        for param in self.required_params:
            if param not in params:
                return utils.bad_req(
                    'parameter {0} is required'.format(param)
                )

        me = request.user.full_url
        if 'me' in params:
            param_me = canonical(params['me'])
            if me != param_me:
                return utils.forbid(
                    'you are logged in as {}, not as {}'.format(me, param_me)
                )

        redirect_uri = urljoin(params['client_id'], params['redirect_uri'])

        type = params['response_type']
        if type not in ('id', 'code'):
            return utils.bad_req(
                'unknown response_type: {0}'.format(type)
            )

        scopes = ()
        if type == 'code':
            if 'scope' not in params:
                return utils.bad_req(
                    'scopes required for code type'
                )
            scopes = params['scope'].split(' ')

        client = requests.mf2(params['client_id'])
        rels = (client.to_dict()['rel-urls']
                .get(redirect_uri, {})
                .get('rels', ()))
        verified = 'redirect_uri' in rels

        try:
            app = client.to_dict(filter_by_type='h-x-app')[0]['properties']
        except IndexError:
            app = None

        return {
            'app': app,
            'me': me,
            'redirect_uri': redirect_uri,
            'verified': verified,
            'params': params,
            'scopes': scopes,
            'title': 'indieauth from {client_id}'.format(**params),
        }

    def post(self, request):
        post = request.POST.dict()
        try:
            code = IndieAuthCode.objects.get(pk=post.get('code'))
        except IndieAuthCode.DoesNotExist:
            # if anything at all goes wrong when decoding the auth code, bail
            # out immediately.
            return utils.forbid('invalid auth code')
        code.delete()
        if code.expired:
            return utils.forbid('invalid auth code')

        if code.response_type != 'id':
            return utils.bad_req(
                'this endpoint only supports response_type=id'
            )
        if code.client_id != post.get('client_id'):
            return utils.forbid('client id did not match')
        if code.redirect_uri != post.get('redirect_uri'):
            return utils.forbid('redirect uri did not match')

        # If we got here, it's valid! Yay!
        return utils.choose_type(request, {'me': code.me}, {
            'application/x-www-form-urlencoded': utils.form_encoded_response,
            'application/json': JsonResponse,
        })


@login_required
@require_POST
def approve(request):
    params = {
        'me': urljoin(utils.origin(request), request.user.url),
        'code': tokens.gen_auth_code(request),
    }
    if 'state' in request.POST:
        params['state'] = request.POST['state']

    uri = request.POST['redirect_uri']
    sep = '&' if '?' in uri else '?'
    return redirect(uri + sep + urlencode(params))
