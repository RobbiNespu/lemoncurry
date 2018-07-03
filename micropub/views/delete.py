from django.http import HttpResponse
from ronkyuu import webmention

from entries.from_url import from_url
from entries.jobs import ping_hub, send_mentions

from .. import error

def delete(request):
    normalise = {
        'application/json': lambda r: r.json.get('url'),
        'application/x-www-form-urlencoded': lambda r: r.POST.get('url'),
    }
    if 'delete' not in request.token:
        raise error.bad_scope('delete')
    if request.content_type not in normalise:
        raise error.unsupported_type(request.content_type)
    url = normalise[request.content_type](request)
    entry = from_url(url)

    if entry.author != request.token.user:
        raise error.forbid('entry belongs to another user')

    perma = entry.absolute_url
    pings = entry.affected_urls
    mentions = webmention.findMentions(perma)['refs']

    entry.delete()

    ping_hub.delay(*pings)
    send_mentions.delay(perma, mentions)
    return HttpResponse(status=204)
