from django.http import JsonResponse


def forbidden():
    return res('forbidden', 403)


def unauthorized():
    return res('unauthorized', 401)


def bad_req(msg):
    return res('invalid_request', msg=msg)


def bad_type(type):
    msg = 'unsupported request type {0}'.format(type)
    return res('invalid_request', 415, msg)


def bad_scope(scope):
    return res('insufficient_scope', 401, scope=scope)


def res(error, status=400, msg=None, scope=None):
    content = {'error': error}
    if msg:
        content['error_description'] = msg
    if scope:
        content['scope'] = scope
    return JsonResponse(content, status=status)
