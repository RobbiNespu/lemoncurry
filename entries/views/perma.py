from annoying.decorators import render_to
from django.shortcuts import redirect
from ..models import Entry


@render_to('entries/entry.html')
def entry(request, kind, id, slug=None):
    entry = Entry.objects.get(pk=id)
    if request.path != entry.url:
        return redirect(entry.url, permanent=True)
    return {
        'entry': entry,
        'title': entry.title,
        'meta': entry.as_meta(request)
    }


@render_to('entries/entry_amp.html')
def entry_amp(request, kind, id, slug=None):
    entry = Entry.objects.get(pk=id)
    if request.path != entry.amp_url:
        return redirect(entry.amp_url, permanent=True)
    return {'entry': entry}
