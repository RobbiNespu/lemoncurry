from annoying.decorators import render_to
from django.shortcuts import redirect, get_object_or_404
from ..models import Entry


@render_to('entries/entry.html')
def entry(request, kind, id, slug=None):
    entry = get_object_or_404(Entry, pk=id)
    if request.path != entry.url:
        return redirect(entry.url, permanent=True)
    return {
        'entry': entry,
        'title': entry.title,
    }
