class Note:
    id = 'note'
    icon = 'fa fa-paper-plane'
    plural = 'notes'


class Article:
    id = 'article'
    icon = 'fa fa-file-text'
    plural = 'articles'


all = (Note, Article)
from_id = {k.id: k for k in all}
from_plural = {k.plural: k for k in all}
