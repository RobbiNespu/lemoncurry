from django.http import HttpResponse, HttpResponseRedirect
from PIL import Image

from lemoncurry import utils
from .models import User


def try_libravatar_org(hash, get):
    url = 'https://seccdn.libravatar.org/avatar/' + hash
    if get:
        url += '?' + get.urlencode()
    return HttpResponseRedirect(url)


def libravatar(request, hash):
    g = request.GET
    size = g.get('s', g.get('size', 80))
    try:
        size = int(size)
    except ValueError:
        return utils.bad_req('size parameter must be an integer')
    if not 1 <= size <= 128:
        return utils.bad_req('size parameter must be between 1 and 128')

    if len(hash) == 32:
        where = {'email_md5': hash}
    elif len(hash) == 64:
        where = {'email_sha256': hash}
    else:
        return utils.bad_req('hash must be either md5 or sha256')

    # If the user doesn't exist or lacks an avatar, see if libravatar.org has
    # one for them - libravatar.org falls back to Gravatar when possible (only
    # for MD5 hashes, since Gravatar doesn't support SHA-256), so this ensures
    # all the most likely places are checked.
    try:
        user = User.objects.get(**where)
    except User.DoesNotExist:
        return try_libravatar_org(hash, g)

    if not user.avatar:
        return try_libravatar_org(hash, g)

    im = Image.open(user.avatar)
    im_resized = im.resize((size, size))

    response = HttpResponse(content_type='image/'+im.format.lower())
    im_resized.save(response, im.format)
    return response
