from django.contrib.auth import get_user_model
from django.http import HttpResponse
from django.urls import reverse
from django.utils.decorators import method_decorator
from django.views import View
from django.views.decorators.csrf import csrf_exempt
from urllib.parse import urljoin

from entries.jobs import ping_hub, send_mentions
from entries.models import Entry
from entries.kinds import Article, Note, Reply, Like, Repost
from lemoncurry import utils
from lemonauth import tokens


@method_decorator(csrf_exempt, name='dispatch')
class MicropubView(View):
    def post(self, request):
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
        entry = Entry(author=user)
        kind = Note
        if 'name' in post:
            entry.name = post['name']
            kind = Article
        if 'content' in post:
            entry.content = post['content']
        if 'in-reply-to' in post:
            entry.in_reply_to = post['in-reply-to']
            kind = Reply
        if 'like-of' in post:
            entry.like_of = post['like-of']
            kind = Like
        if 'repost-of' in post:
            entry.repost_of = post['repost-of']
            kind = Repost

        entry.kind = kind.id
        entry.save()

        base = utils.origin(request)
        perma = urljoin(base, entry.url)
        others = (urljoin(base, url) for url in (
            reverse('home:index'),
            reverse('entries:atom'),
            reverse('entries:rss'),
            reverse('entries:' + kind.index),
            reverse('entries:' + kind.atom),
            reverse('entries:' + kind.rss),
        ))
        ping_hub.delay(perma, *others)
        send_mentions.delay(perma)

        res = HttpResponse(status=201)
        res['Location'] = perma
        return res


micropub = MicropubView.as_view()
