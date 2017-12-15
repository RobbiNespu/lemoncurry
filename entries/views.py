from annoying.decorators import render_to
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse
from .models import Entry, Cat
from .pagination import paginate


@render_to('entries/index.html')
def index(request, kind, page):
    def url(page):
        kwargs = {'page': page} if page > 1 else {}
        return reverse('entries:' + kind.index, kwargs=kwargs)

    entries = Entry.objects.filter(kind=kind.id)
    entries = paginate(queryset=entries, reverse=url, page=page)
    if hasattr(entries, 'content'):
        return entries

    return {
        'entries': entries,
        'atom': 'entries:' + kind.atom,
        'rss': 'entries:' + kind.rss,
        'title': kind.plural,
    }


@render_to('entries/index.html')
def cat(request, slug, page):
    def url(page):
        kwargs = {'slug': slug}
        if page > 1:
            kwargs['page'] = page
        return reverse('entries:cat', kwargs=kwargs)

    cat = get_object_or_404(Cat, slug=slug)
    entries = cat.entries.all()
    entries = paginate(queryset=entries, reverse=url, page=page)
    if hasattr(entries, 'content'):
        return entries

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
