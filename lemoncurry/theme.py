from django.conf import settings
from os.path import join
from yaml import safe_load

path = join(
    settings.BASE_DIR,
    'lemoncurry', 'static',
    'base16-materialtheme-scheme', 'material-darker.yaml',
)
with open(path, 'r') as f:
    theme = safe_load(f)


def color(i):
    return '#' + theme['base0' + format(i, '1X')]
