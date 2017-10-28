from django.conf import settings
from django.http import JsonResponse
from favicon.models import FaviconImg
from lemoncurry import utils
from lemoncurry.theme import theme
from urllib.parse import urljoin


def manifest(request):
    origin = utils.origin(request)
    app = {
        'name': settings.LEMONCURRY_SITE_NAME,
        'background_color': '#' + theme['base00'],
        'theme_color': '#' + theme['base02'],
    }

    rels = ('shortcut icon', 'apple-touch-icon')
    icons = FaviconImg.objects.filter(
        faviconFK__isFavicon=True,
        rel__in=rels,
    ).order_by('size')
    app['icons'] = [{
        'type': 'image/png',
        'size': '{0}x{0}'.format(icon.size),
        'src': urljoin(origin, icon.faviconImage.url),
    } for icon in icons]

    return JsonResponse(app, content_type='application/manifest+json')
