from annoying.decorators import render_to
from django.shortcuts import get_object_or_404
from django.urls import reverse
from ..models import Entry, Cat
from ..pagination import paginate


@render_to('entries/index.html')
def by_kind(request, kind, page=None):
    entries = Entry.objects.filter(kind=kind.id)
    entries = paginate(queryset=entries, reverse=kind.index_page, page=page)

    return {
        'entries': entries,
        'atom': kind.atom,
        'rss': kind.rss,
        'title': kind.plural,
    }


@render_to('entries/index.html')
def by_cat(request, slug, page=None):
    def url(page):
        kwargs = {'slug': slug}
        if page > 1:
            kwargs['page'] = page
        return reverse('entries:cat', kwargs=kwargs)

    cat = get_object_or_404(Cat, slug=slug)
    entries = cat.entries.all()
    entries = paginate(queryset=entries, reverse=url, page=page)

    return {
        'entries': entries,
        'title': '#' + cat.name,
    }
