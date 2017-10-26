import mf2py

from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden, HttpResponseBadRequest
from django.shortcuts import render
from django.utils.decorators import method_decorator
from django.views.generic import TemplateView
from lemoncurry import breadcrumbs

breadcrumbs.add('lemonauth:indie', label='indieauth', parent='home:index')


class IndieView(TemplateView):
    template_name = 'lemonauth/indie.html'
    required_params = ('me', 'client_id', 'redirect_uri')

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(IndieView, self).dispatch(*args, **kwargs)

    def get(self, request):
        params = request.GET
        for param in self.required_params:
            if param not in params:
                return HttpResponseBadRequest(
                    'parameter {0} is required'.format(param),
                    content_type='text/plain',
                )

        me = params['me']
        user = '{0}://{1}{2}'.format(
            request.scheme,
            request.META['HTTP_HOST'],
            request.user.url
        )
        if me != user:
            return HttpResponseForbidden(
                'you are logged in but not as {0}'.format(me),
                content_type='text/plain',
            )

        client = mf2py.parse(url=params['client_id'])
        rels = client['rel-urls'].get(params['redirect_uri'], {}).get('rels', ())
        if 'redirect_uri' not in rels:
            return HttpResponseBadRequest(
                'your redirect_uri is not published on your client_id page',
                content_type='text/plain'
            )

        return render(request, self.template_name, {
            'params': params,
            'title': 'indieauth',
        })
