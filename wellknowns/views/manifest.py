from django.http import JsonResponse
from django.urls import reverse
from ..favicons import icons
from lemoncurry import utils
from lemoncurry.theme import color
from urllib.parse import urljoin
from textwrap import shorten


def manifest_icons(base):
    return [{'src': i.url, 'type': i.mime, 'sizes': i.sizes} for i in sorted(icons, key=lambda i: i.size)]


def manifest(request):
    base = utils.origin(request)
    start_url = reverse('home:index') + '?utm_source=homescreen'

    app = {
        'name': request.site.name,
        'short_name': shorten(request.site.name, width=20, placeholder=''),
        'icons': manifest_icons(base),

        'display': 'browser',
        'start_url': urljoin(base, start_url),

        'background_color': color(0),
        'theme_color': color(10),
    }

    return JsonResponse(app, content_type='application/manifest+json')
