from annoying.decorators import render_to
from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from django.urls import reverse
from users.models import User
from lemoncurry import breadcrumbs, utils
from urllib.parse import urljoin

breadcrumbs.add('home:index', 'home')


@render_to('home/index.html')
def index(request):
    query = User.objects.prefetch_related('entries', 'profiles', 'keys')
    user = get_object_or_404(query, pk=1)

    return {
        'user': user,
        'entries': user.entries.all(),
        'atom': 'entries:atom',
        'rss': 'entries:rss',
        'meta': user.as_meta(request),
    }


def robots(request):
    base = utils.origin(request)
    lines = (
        'User-agent: *',
        'Sitemap: {0}'.format(urljoin(base, reverse('sitemap')))
    )
    return HttpResponse("\n".join(lines) + "\n", content_type='text/plain')
