from django.core.paginator import Paginator
from django.shortcuts import redirect


def paginate(queryset, reverse, page):
    class Page:
        def __init__(self, i):
            self.i = i

        @property
        def url(self):
            return reverse(self.i)

        @property
        def current(self):
            return self.i == entries.number

    # If the first page was requested, redirect to the clean version of the URL
    # with no page suffix.
    if page == '1':
        return redirect(Page(1).url)

    paginator = Paginator(queryset, 2)
    entries = paginator.page(page or 1)

    entries.pages = tuple(Page(i) for i in paginator.page_range)

    if entries.has_previous():
        entries.prev = Page(entries.previous_page_number())
    if entries.has_next():
        entries.next = Page(entries.next_page_number())

    return entries
