class Entry:
    def __init__(self, id, plural, icon, slug=False):
        self.id = id
        self.plural = plural
        self.icon = icon
        self.slug = slug

    @property
    def index(self):
        return self.plural + '_index'

    @property
    def entry(self):
        return self.plural + '_entry'

    @property
    def atom(self):
        return self.plural + '_atom'

    @property
    def rss(self):
        return self.plural + '_rss'


Note = Entry(
    id='note',
    icon='fa fa-paper-plane',
    plural='notes',
)


Article = Entry(
    id='article',
    icon='fa fa-file-text',
    plural='articles',
    slug=True,
)

Photo = Entry(
    id='photo',
    icon='fa fa-camera',
    plural='photos',
)

Reply = Entry(
    id='reply',
    icon='fa fa-comment',
    plural='replies',
)

Like = Entry(
    id='like',
    icon='fa fa-heart',
    plural='likes',
)

Repost = Entry(
    id='repost',
    icon='fa fa-retweet',
    plural='reposts',
)

all = (Note, Article, Photo, Reply, Like, Repost)
from_id = {k.id: k for k in all}
from_plural = {k.plural: k for k in all}
