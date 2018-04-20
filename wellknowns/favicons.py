from itertools import chain
from django.core.files.storage import default_storage


class Favicon:
    def __init__(self, size, rel='icon', mime='image/png'):
        self.rel = rel
        self.mime = mime
        if not isinstance(size, tuple):
            size = (size, size)
        self.size = size

    @property
    def url(self):
        return default_storage.url('favicon/' + self.filename)

    @property
    def filename(self):
        return 'favicon-{0}.png'.format(*self.size)

    @property
    def sizes(self):
        return 'x'.join(str(s) for s in self.size)


tile_sizes = {'small': 128, 'medium': 270, 'wide': (558, 270), 'large': 558}


class Tile(Favicon):
    def __init__(self, size_name):
        super().__init__(tile_sizes[size_name])
        self.size_name = size_name

    @property
    def filename(self):
        return '{0}tile.png'.format(self.size_name)


sizes = (32, 57, 76, 96, 120, 128, 144, 180, 195, 228)
icons = tuple(chain(
    (Favicon(s) for s in sizes),
    (Tile(s) for s in tile_sizes.keys()),
    (Favicon(152, rel='apple-touch-icon-precomposed'),
     Favicon(196, rel='shortcut icon'))
))
