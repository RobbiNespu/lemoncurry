import json

from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods

from lemonauth import tokens

from .create import create
from .delete import delete
from .query import query

actions = {
    'create': create,
    'delete': delete,
}


@csrf_exempt
@require_http_methods(['GET', 'HEAD', 'POST'])
def micropub(request):
    request.token = tokens.auth(request)
    if request.method in ('GET', 'HEAD'):
        return query(request)

    action = request.POST.get('action', 'create')
    if request.content_type == 'application/json':
        request.json = json.load(request)
        action = request.json.get('action', 'create')
    if action in actions:
        return actions[action](request)
    return error.bad_req('unknown action: {}'.format(action))
