from django.http import HttpRequest, HttpResponse
from django.utils.deprecation import MiddlewareMixin


class ResponseException(Exception):
    def __init__(self, response: HttpResponse) -> None:
        self.response = response


class ResponseExceptionMiddleware(MiddlewareMixin):
    def process_exception(self, request: HttpRequest, exception: Exception) -> HttpResponse:
        if isinstance(exception, ResponseException):
            return exception.response
        raise exception
