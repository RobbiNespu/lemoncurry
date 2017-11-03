import mf2py

from annoying.decorators import render_to
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.shortcuts import redirect
from django.utils.decorators import method_decorator
from django.views.generic import TemplateView
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
from lemoncurry import breadcrumbs, utils
from urllib.parse import urlencode, urljoin, urlunparse, urlparse

from .. import tokens

breadcrumbs.add('lemonauth:indie', label='indieauth', parent='home:index')


def canonical(url):
    (scheme, loc, path, params, q, fragment) = urlparse(url)
    if not path:
        path = '/'
    if not loc:
        loc, path = path, ''
    if not scheme:
        scheme = 'https'
    return urlunparse((scheme, loc, path, params, q, fragment))


@method_decorator(csrf_exempt, name='dispatch')
class IndieView(TemplateView):
    template_name = 'lemonauth/indie.html'
    required_params = ('me', 'client_id', 'redirect_uri')

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

        me = canonical(params['me'])
        user = urljoin(utils.origin(request), request.user.url)
        if user != me:
            return utils.forbid(
                'you are logged in but not as {0}'.format(me)
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

        client = mf2py.Parser(url=params['client_id'], html_parser='html5lib')
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
            'title': 'indieauth',
        }

    def post(self, request):
        post = request.POST.dict()
        try:
            code = tokens.verify_auth_code(post.get('code'))
        except Exception:
            # if anything at all goes wrong when decoding the auth code, bail
            # out immediately.
            return utils.forbid('invalid auth code')

        if code['response_type'] != 'id':
            return utils.bad_req(
                'this endpoint only supports response_type=id'
            )
        if post.get('client_id') != code['client_id']:
            return utils.forbid('client id did not match')
        if post.get('redirect_uri') != code['redirect_uri']:
            return utils.forbid('redirect uri did not match')

        # If we got here, it's valid! Yay!
        return utils.choose_type(request, {'me': code['me']}, {
            'application/x-www-form-urlencoded': utils.form_encoded_response,
            'application/json': JsonResponse,
        })


@login_required
@require_POST
def approve(request):
    post = request.POST
    params = tokens.gen_auth_code(post)

    uri = post['redirect_uri']
    sep = '&' if '?' in uri else '?'
    return redirect(uri + sep + urlencode(params))
