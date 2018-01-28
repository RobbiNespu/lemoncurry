from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods

from lemonauth import tokens

from .create import create
from .query import query


@csrf_exempt
@require_http_methods(['GET', 'HEAD', 'POST'])
def micropub(request):
    token = tokens.auth(request)
    if hasattr(token, 'content'):
        return token
    request.token = token
    if request.method == 'POST':
        return create(request)
    if request.method in ('GET', 'HEAD'):
        return query(request)
