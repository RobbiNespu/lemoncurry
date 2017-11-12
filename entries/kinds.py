class Entry:
    def __init__(self, id, plural, icon, on_home=True, slug=False):
        self.id = id
        self.plural = plural
        self.icon = icon
        self.on_home = on_home
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
    on_home=False,
)

Like = Entry(
    id='like',
    icon='fa fa-heart',
    plural='likes',
    on_home=False,
)

Repost = Entry(
    id='repost',
    icon='fa fa-retweet',
    plural='reposts',
)

all = (Note, Article, Photo, Reply, Like, Repost)
on_home = {k.id for k in all if k.on_home}
from_id = {k.id: k for k in all}
from_plural = {k.plural: k for k in all}
