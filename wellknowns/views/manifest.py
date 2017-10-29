from django.http import JsonResponse
from django.urls import reverse
from favicon.models import FaviconImg
from lemoncurry import utils
from lemoncurry.theme import color
from urllib.parse import urljoin
from textwrap import shorten


def manifest(request):
    base = utils.origin(request)
    start_url = reverse('home:index') + '?utm_source=homescreen'

    app = {
        'name': request.site.name,
        'short_name': shorten(request.site.name, width=20, placeholder=''),

        'display': 'browser',
        'start_url': urljoin(base, start_url),

        'background_color': color(0),
        'theme_color': color(2),
    }

    rels = ('shortcut icon', 'apple-touch-icon')
    icons = FaviconImg.objects.filter(
        faviconFK__isFavicon=True,
        rel__in=rels,
    ).order_by('size')
    app['icons'] = [{
        'type': 'image/png',
        'sizes': '{0}x{0}'.format(icon.size),
        'src': urljoin(base, icon.faviconImage.url),
    } for icon in icons]

    return JsonResponse(app, content_type='application/manifest+json')
