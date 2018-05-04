from annoying.decorators import render_to
from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from django.urls import reverse
from users.models import User
from urllib.parse import urljoin

from entries import kinds, pagination
from lemoncurry import breadcrumbs, utils

breadcrumbs.add('home:index', 'home')


@render_to('home/index.html')
def index(request, page=None):
    def url(page):
        kwargs = {'page': page} if page != 1 else {}
        return reverse('home:index', kwargs=kwargs)

    user = request.user
    if not hasattr(user, 'entries'):
        user = get_object_or_404(User, pk=1)

    entries = user.entries.filter(kind__in=kinds.on_home)
    entries = pagination.paginate(queryset=entries, reverse=url, page=page)

    # If we got a valid HTTP response, just return it without rendering.
    if hasattr(entries, 'content'):
        return entries

    return {
        'user': user,
        'entries': entries,
        'atom': reverse('entries:atom'),
        'rss': reverse('entries:rss'),
        'meta': user.as_meta(request),
    }


def robots(request):
    base = utils.origin(request)
    lines = (
        'User-agent: *',
        'Sitemap: {0}'.format(urljoin(base, reverse('sitemap')))
    )
    return HttpResponse("\n".join(lines) + "\n", content_type='text/plain')
