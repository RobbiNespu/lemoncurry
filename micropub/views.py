import json
from django.http import HttpResponse
from django.urls import reverse
from django.utils.decorators import method_decorator
from django.views import View
from django.views.decorators.csrf import csrf_exempt
from urllib.parse import urljoin

from entries.jobs import ping_hub, send_mentions
from entries.models import Cat, Entry
from entries.kinds import Article, Note, Reply, Like, Repost
from lemoncurry import utils
from lemonauth import tokens


def form_to_mf2(request):
    properties = {}
    post = request.POST
    for key in post.keys():
        if key.endswith('[]'):
            key = key[:-2]
        if key == 'access_token':
            continue
        properties[key] = post.getlist(key) + post.getlist(key + '[]')

    type = []
    if 'h' in properties:
        type = ['h-' + p for p in properties['h']]
        del properties['h']
    return {'type': type, 'properties': properties}


@method_decorator(csrf_exempt, name='dispatch')
class MicropubView(View):
    def post(self, request):
        token = tokens.auth(request)
        if hasattr(token, 'content'):
            return token

        normalise = {
            'application/json': json.load,
            'application/x-www-form-urlencoded': form_to_mf2,
        }
        if request.content_type not in normalise:
            return HttpResponse(
                'unsupported request type {0}'.format(request.content_type),
                content_type='text/plain',
                status=415,
            )
        body = normalise[request.content_type](request)
        if 'type' not in body:
            return utils.bad_req('mf2 object type required')
        if body['type'] != ['h-entry']:
            return utils.bad_req('only h-entry supported')

        entry = Entry(author=token.user)
        props = body.get('properties', {})
        kind = Note
        if 'name' in props:
            entry.name = '\n'.join(props['name'])
            kind = Article
        if 'content' in props:
            entry.content = '\n'.join(
                c if isinstance(c, str) else c['html']
                for c in props['content']
            )
        if 'in-reply-to' in props:
            entry.in_reply_to = props['in-reply-to']
            kind = Reply
        if 'like-of' in props:
            entry.like_of = props['like-of']
            kind = Like
        if 'repost-of' in props:
            entry.repost_of = props['repost-of']
            kind = Repost

        cats = [Cat.objects.from_name(c) for c in props.get('category', [])]

        entry.kind = kind.id
        entry.save()
        entry.cats = cats
        entry.save()

        base = utils.origin(request)
        perma = urljoin(base, entry.url)
        others = [urljoin(base, url) for url in (
            reverse('home:index'),
            reverse('entries:atom'),
            reverse('entries:rss'),
            reverse('entries:' + kind.index),
            reverse('entries:' + kind.atom),
            reverse('entries:' + kind.rss),
        )] + [urljoin(base, cat.url) for cat in cats]
        ping_hub.delay(perma, *others)
        send_mentions.delay(perma)

        res = HttpResponse(status=201)
        res['Location'] = perma
        return res


micropub = MicropubView.as_view()
