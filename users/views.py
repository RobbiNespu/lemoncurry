from django.db.models import Q
from django.http import HttpResponse, HttpResponseRedirect
from django.views.decorators.cache import cache_page
from PIL import Image

from lemoncurry import utils
from .models import User


def try_libravatar_org(hash, get):
    url = 'https://seccdn.libravatar.org/avatar/' + hash
    if get:
        url += '?' + get.urlencode()
    return HttpResponseRedirect(url)


@cache_page(60 * 15)
def libravatar(request, hash):
    g = request.GET
    size = g.get('s', g.get('size', 80))
    try:
        size = int(size)
    except ValueError:
        size = 80
    if not 1 <= size <= 512:
        size = 512

    if len(hash) == 32:
        where = Q(email_md5=hash)
    elif len(hash) == 64:
        where = Q(email_sha256=hash) | Q(openid_sha256=hash)
    else:
        return utils.bad_req('hash must be either md5 or sha256')

    # If the user doesn't exist or lacks an avatar, see if libravatar.org has
    # one for them - libravatar.org falls back to Gravatar when possible (only
    # for MD5 hashes, since Gravatar doesn't support SHA-256), so this ensures
    # all the most likely places are checked.
    try:
        user = User.objects.get(where)
    except User.DoesNotExist:
        return try_libravatar_org(hash, g)

    if not user.avatar:
        return try_libravatar_org(hash, g)

    im = Image.open(user.avatar)
    image_type = im.format
    natural_size = min(im.size)

    im = im.crop((0, 0, natural_size, natural_size))
    im = im.resize((size, size), resample=Image.HAMMING)

    response = HttpResponse(content_type='image/'+image_type.lower())
    im.save(response, image_type)
    return response
