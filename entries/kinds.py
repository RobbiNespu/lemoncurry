class Entry:
    fields = ()

    @classmethod
    def has(cls, field):
        return field in cls.fields


class Note(Entry):
    id = 'note'
    icon = 'fa fa-paper-plane'
    plural = 'notes'


class Article(Entry):
    id = 'article'
    icon = 'fa fa-file-text'
    plural = 'articles'
    fields = ('slug', 'name')


all = (Note, Article)
from_id = {k.id: k for k in all}
from_plural = {k.plural: k for k in all}
