from django.contrib.auth import get_user_model
from django.http import HttpResponse
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
from urllib.parse import urljoin

from entries.jobs import ping_hub
from entries.models import Entry
from entries.kinds import Article, Note
from lemoncurry import utils
from lemonauth import tokens


@csrf_exempt
@require_POST
def micropub(request):
    auth = request.META.get('HTTP_AUTHORIZATION', '').split(' ')
    if auth[0] != 'Bearer':
        return utils.bad_req('only Bearer auth supported')
    try:
        token = tokens.decode(auth[1])
    except Exception:
        return utils.forbid('invalid token')
    user = get_user_model().objects.get(pk=token['uid'])

    post = request.POST
    if post.get('h') != 'entry':
        return utils.bad_req('only h=entry supported')
    entry = Entry(author=user, kind=Note.id)
    if 'name' in post:
        entry.name = post['name']
        entry.kind = Article.id
    if 'content' in post:
        entry.content = post['content']

    entry.save()

    base = utils.origin(request)
    perma = urljoin(base, entry.url)
    others = (urljoin(base, url) for url in (
        reverse('home:index'),
        reverse('entries:atom'),
        reverse('entries:rss'),
    ))
    ping_hub(perma, *others)

    res = HttpResponse(status=201)
    res['Location'] = perma
    return res
