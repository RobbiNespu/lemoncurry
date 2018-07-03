from django.http import JsonResponse
from lemoncurry.middleware import ResponseException
from typing import Optional


def forbidden() -> ResponseException:
    return res('forbidden', 403)


def unauthorized() -> ResponseException:
    return res('unauthorized', 401)


def bad_req(msg: str) -> ResponseException:
    return res('invalid_request', msg=msg)


def bad_type(type: str) -> ResponseException:
    msg = 'unsupported request type {0}'.format(type)
    return res('invalid_request', 415, msg)


def bad_scope(scope: str) -> ResponseException:
    return res('insufficient_scope', 401, scope=scope)


def res(error: str,
        status: Optional[int]=400,
        msg: Optional[str]=None,
        scope: Optional[str]=None):
    content = {'error': error}
    if msg is not None:
        content['error_description'] = msg
    if scope:
        content['scope'] = scope
    return ResponseException(JsonResponse(content, status=status))
