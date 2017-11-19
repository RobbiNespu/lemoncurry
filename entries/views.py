from annoying.decorators import render_to
from django.shortcuts import get_object_or_404, redirect
from .models import Entry, Tag


@render_to('entries/index.html')
def index(request, kind):
    entries = Entry.objects.filter(kind=kind.id)
    return {
        'entries': entries,
        'atom': 'entries:' + kind.atom,
        'rss': 'entries:' + kind.rss,
        'title': kind.plural,
    }


@render_to('entries/index.html')
def tagged(request, slug):
    tag = get_object_or_404(Tag, slug=slug)
    return {
        'entries': tag.entries.all(),
        'title': '#' + tag.name,
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
