import json
from django.urls import reverse
from django.http import HttpResponse
from urllib.parse import urljoin

from entries.jobs import ping_hub, send_mentions
from entries.models import Cat, Entry
from entries.kinds import Article, Note, Reply, Like, Repost
from lemoncurry import utils

from . import error


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


def create(request):
    normalise = {
        'application/json': json.load,
        'application/x-www-form-urlencoded': form_to_mf2,
    }
    if 'create' not in request.token:
        return error.bad_scope('create')
    if request.content_type not in normalise:
        return error.unsupported_type(request.content_type)
    body = normalise[request.content_type](request)
    if 'type' not in body:
        return error.bad_req('mf2 object type required')
    if body['type'] != ['h-entry']:
        return error.bad_req('only h-entry supported')

    entry = Entry(author=request.token.user)
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
    entry.cats.set(cats)
    entry.save()

    base = utils.origin(request)
    perma = urljoin(base, entry.url)
    others = [urljoin(base, url) for url in (
        reverse('home:index'),
        reverse('entries:atom'),
        reverse('entries:rss'),
        reverse('entries:index', kwargs={'kind': kind.plural}),
        reverse('entries:atom_by_kind', kwargs={'kind': kind.plural}),
        reverse('entries:rss_by_kind', kwargs={'kind': kind.plural}),
    )] + [urljoin(base, cat.url) for cat in cats]
    ping_hub.delay(perma, *others)
    send_mentions.delay(perma)

    res = HttpResponse(status=201)
    res['Location'] = perma
    return res
