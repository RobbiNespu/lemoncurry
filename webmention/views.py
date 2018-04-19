from django.http import HttpResponse
from django.urls import resolve, reverse, Resolver404
from django.shortcuts import get_object_or_404
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_GET, require_POST
from entries.models import Entry
from lemoncurry.utils import bad_req
from urllib.parse import urljoin, urlparse

from .models import State, Webmention


@csrf_exempt
@require_POST
def accept(request):
    if 'source' not in request.POST:
        return bad_req('missing source url')
    source_url = request.POST['source']

    if 'target' not in request.POST:
        return bad_req('missing target url')
    target_url = request.POST['target']

    source = urlparse(source_url)
    target = urlparse(target_url)
    if source.scheme not in ('http', 'https'):
        return bad_req('unsupported source scheme')
    if target.scheme not in ('http', 'https'):
        return bad_req('unsupported target scheme')
    if target.netloc != request.site.domain:
        return bad_req('target not on this site')
    origin = 'https://' + target.netloc

    try:
        match = resolve(target.path)
    except Resolver404:
        return bad_req('target not found')

    if match.view_name != 'entries:entry':
        return bad_req('target does not accept webmentions')

    try:
        entry = Entry.objects.get(pk=match.kwargs['id'])
    except Entry.DoesNotExist:
        return bad_req('target not found')

    try:
        mention = Webmention.objects.get(source=source_url, target=target_url)
    except Webmention.DoesNotExist:
        mention = Webmention()
        mention.source = source_url
        mention.target = target_url

    mention.entry = entry
    mention.state = State.PENDING
    mention.save()
    status_url = reverse('webmention:status', kwargs={'id': mention.id})

    res = HttpResponse(status=201)
    res['Location'] = urljoin(origin, status_url)
    return res


@require_GET
def status(request, mention_id):
    mention = get_object_or_404(Webmention.objects, pk=mention_id)
    return HttpResponse(mention.get_state_display())
