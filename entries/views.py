from django.shortcuts import redirect, render
from .models import Entry


def index(request, kind):
    entries = Entry.objects.filter(kind=kind.id)
    return render(request, 'entries/index.html', {
        'entries': entries,
        'title': kind.plural
    })


def entry(request, id, slug=None):
    entry = Entry.objects.get(pk=id)
    if request.path != entry.url:
        return redirect(entry.url, permanent=True)
    return render(request, 'entries/entry.html', {
        'entry': entry,
        'title': entry.title,
        'meta': entry.as_meta(request)
    })
