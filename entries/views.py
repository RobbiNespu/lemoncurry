from django.shortcuts import render
from .models import Entry


def index(request, kind):
    entries = Entry.objects.filter(kind=kind.id)
    return render(request, 'entries/index.html', {
        'entries': entries,
        'title': kind.plural
    })


def entry(request, id, slug=None):
    entry = Entry.objects.get(pk=id)
    return render(request, 'entries/entry.html', {
        'entry': entry,
        'title': entry.name or entry.content,
        'meta': entry.as_meta(request)
    })
