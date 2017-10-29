import mf2py

from annoying.decorators import render_to
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden, HttpResponseBadRequest
from django.http import JsonResponse
from django.utils.decorators import method_decorator
from django.views.generic import TemplateView
from django.views.decorators.http import require_POST
from lemoncurry import breadcrumbs, utils
from urllib.parse import urljoin, urlunparse, urlparse

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
                return HttpResponseBadRequest(
                    'parameter {0} is required'.format(param),
                    content_type='text/plain',
                )

        me = canonical(params['me'])
        user = urljoin(utils.origin(request), request.user.url)
        if user != me:
            return HttpResponseForbidden(
                'you are logged in but not as {0}'.format(me),
                content_type='text/plain',
            )

        client = mf2py.Parser(url=params['client_id'], html_parser='html5lib')
        rels = (client.to_dict()['rel-urls']
                .get(params['redirect_uri'], {})
                .get('rels', ()))
        if 'redirect_uri' not in rels:
            return HttpResponseBadRequest(
                'your redirect_uri is not published on your client_id page',
                content_type='text/plain'
            )

        try:
            app = client.to_dict(filter_by_type='h-x-app')[0]['properties']
        except IndexError:
            app = None

        return {'app': app, 'me': me, 'params': params, 'title': 'indieauth'}


@login_required
@require_POST
def approve(request):
    return JsonResponse(request.POST)
