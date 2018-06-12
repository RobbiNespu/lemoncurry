from micropub.views import error
from .models import IndieAuthCode, Token


def auth(request):
    if 'HTTP_AUTHORIZATION' in request.META:
        auth = request.META.get('HTTP_AUTHORIZATION').split(' ')
        if auth[0] != 'Bearer':
            return error.bad_req('auth type {0} not supported'.format(auth[0]))
        if len(auth) != 2:
            return error.bad_req(
                'invalid Bearer auth format, must be Bearer <token>'
            )
        token = auth[1]
    elif 'access_token' in request.POST:
        token = request.POST.get('access_token')
    elif 'access_token' in request.GET:
        token = request.GET.get('access_token')
    else:
        return error.unauthorized()

    try:
        token = Token.objects.get(pk=token)
    except Token.DoesNotExist:
        return error.forbidden()

    return token


def gen_auth_code(req):
    code = IndieAuthCode()
    code.user = req.user
    code.client_id = req.POST['client_id']
    code.redirect_uri = req.POST['redirect_uri']
    code.response_type = req.POST.get('response_type', 'id')
    if 'scope' in req.POST:
        code.scope = ' '.join(req.POST.getlist('scope'))
    code.save()
    return code.id


def gen_token(code):
    tok = Token()
    tok.user = code.user
    tok.client_id = code.client_id
    tok.scope = code.scope
    tok.save()
    return tok.id
