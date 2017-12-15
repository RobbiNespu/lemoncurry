from annoying.decorators import render_to
from django.core.paginator import Paginator
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse
from users.models import User
from urllib.parse import urljoin

from entries import kinds
from lemoncurry import breadcrumbs, utils

breadcrumbs.add('home:index', 'home')


@render_to('home/index.html')
def index(request, page):
    query = User.objects.prefetch_related('entries', 'profiles', 'keys')
    user = get_object_or_404(query, pk=1)
    paginator = Paginator(user.entries.filter(kind__in=kinds.on_home), 10)

    # If we explicitly got /page/1 in the URL then redirect to the version with
    # no page suffix.
    if page == '1':
        return redirect('home:index', permanent=True)
    entries = paginator.page(page or 1)

    class Page:
        def __init__(self, i):
            self.i = i

        @property
        def url(self):
            return reverse('home:index', kwargs={'page': self.i})

        @property
        def current(self):
            return self.i == entries.number

    entries.pages = tuple(Page(i) for i in paginator.page_range)
    if entries.has_previous():
        entries.prev = Page(entries.previous_page_number())
    if entries.has_next():
        entries.next = Page(entries.next_page_number())

    return {
        'user': user,
        'entries': entries,
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
