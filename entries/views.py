from annoying.decorators import render_to
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse
from .models import Entry, Cat


@render_to('entries/index.html')
def index(request, kind, before=None):
    entries = Entry.objects.filter(kind=kind.id)
    if before:
        entries = entries.filter(id__lt=before)
    entries = entries[:10]

    next = None
    if entries:
        last = entries.last().id
        next = reverse('entries:' + kind.index, kwargs={'before': last})

    return {
        'entries': entries,
        'next': next,
        'atom': 'entries:' + kind.atom,
        'rss': 'entries:' + kind.rss,
        'title': kind.plural,
    }


@render_to('entries/index.html')
def cat(request, slug, before=None):
    cat = get_object_or_404(Cat, slug=slug)
    entries = cat.entries.all()
    if before:
        entries = entries.filter(id__lt=before)
    entries = entries[:10]

    next = None
    if entries:
        next = reverse('entries:cat', kwargs={
            'slug': slug,
            'before': entries.last().id
        })
    return {
        'entries': entries,
        'next': next,
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
