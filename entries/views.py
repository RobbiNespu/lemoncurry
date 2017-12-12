from annoying.decorators import render_to
from django.core.paginator import Paginator
from django.shortcuts import get_object_or_404, redirect
from .models import Entry, Cat


@render_to('entries/index.html')
def index(request, kind, page):
    paginator = Paginator(Entry.objects.filter(kind=kind.id), 10)

    # If we explicitly got /page/1 in the URL then redirect to the version with
    # no page suffix.
    if page == '1':
        return redirect('entries:' + kind.index, permanent=True)
    entries = paginator.page(page or 1)

    return {
        'entries': entries,
        'atom': 'entries:' + kind.atom,
        'rss': 'entries:' + kind.rss,
        'title': kind.plural,
    }


@render_to('entries/index.html')
def cat(request, slug, page):
    cat = get_object_or_404(Cat, slug=slug)
    paginator = Paginator(cat.entries.all(), 10)
    if page == '1':
        return redirect('entries:cat', permanent=True, slug=slug)
    entries = paginator.page(page or 1)

    return {
        'entries': entries,
        'title': '#' + cat.name,
    }


@render_to('entries/entry.html')
def entry(request, id, slug=None):
    entry = Entry.objects.get(pk=id)
    if request.path != entry.url:
        return redirect(entry.url, permanent=True)
    return {
        'entry': entry,
        'title': entry.title,
        'meta': entry.as_meta(request)
    }
