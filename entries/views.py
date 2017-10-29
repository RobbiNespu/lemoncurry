from annoying.decorators import render_to
from django.shortcuts import redirect
from .models import Entry


@render_to('entries/index.html')
def index(request, kind):
    entries = Entry.objects.filter(kind=kind.id)
    return {'entries': entries, 'title': kind.plural}


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
