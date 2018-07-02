import hashlib

from django.core.files.storage import default_storage as store
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
import magic

from lemonauth import tokens
from lemoncurry.utils import absolute_url
from . import error

ACCEPTED_MEDIA_TYPES = (
    'image/gif',
    'image/jpeg',
    'image/png',
)


@csrf_exempt
@require_POST
def media(request):
    token = tokens.auth(request)
    if hasattr(token, 'content'):
        return token
    if 'file' not in request.FILES:
        return error.bad_req(
            "a file named 'file' must be provided to the media endpoint"
        )
    file = request.FILES['file']
    if file.content_type not in ACCEPTED_MEDIA_TYPES:
        return error.bad_req(
            'unacceptable file type {0}'.format(file.content_type)
        )

    mime = None
    sha = hashlib.sha256()
    for chunk in file.chunks():
        if mime is None:
            mime = magic.from_buffer(chunk, mime=True)
        sha.update(chunk)

    if mime != file.content_type:
        return error.bad_req(
            'detected file type {0} did not match specified file type {1}'
            .format(mime, file.content_type)
        )

    path = 'mp/{0[0]}/{2}.{1}'.format(*mime.split('/'), sha.hexdigest())
    path = store.save(path, file)
    url = absolute_url(request, store.url(path))

    res = HttpResponse(status=201)
    res['Location'] = url
    return res
