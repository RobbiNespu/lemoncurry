class Entry:
    fields = ()

    def has(self, field):
        return field in self.fields

    def __init__(self, id, plural, icon, fields=()):
        self.id = id
        self.plural = plural
        self.icon = icon
        self.fields = fields

    @property
    def index(self):
        return self.plural + '_index'

    @property
    def entry(self):
        return self.plural + '_entry'

    @property
    def entry_slug(self):
        return self.entry + '_slug'


Note = Entry(
    id='note',
    icon='fa fa-paper-plane',
    plural='notes',
)


Article = Entry(
    id='article',
    icon='fa fa-file-text',
    plural='articles',
    fields=('slug', 'name'),
)


all = (Note, Article)
from_id = {k.id: k for k in all}
from_plural = {k.plural: k for k in all}
