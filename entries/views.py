from django.shortcuts import render
from .models import Entry


def index(request, kind):
    entries = Entry.objects.filter(kind=kind.id)
    return render(request, 'entries/index.html', {
        'entries': entries,
        'title': kind.plural
    })
