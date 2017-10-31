from django.http import HttpResponse, JsonResponse
from django.urls import reverse
from lemoncurry.utils import load_package_json, origin
from urllib.parse import urljoin
from xrd import XRD, Attribute, Element, Link


def add_links(request, dest):
    base = origin(request)
    pkg = load_package_json()
    webfinger = reverse('wellknowns:webfinger') + '?resource={uri}'
    license = 'https://creativecommons.org/licenses/by-sa/4.0/'

    links = (
        Link(
            href=urljoin(base, reverse('lemonauth:indie')),
            rel='authorization_endpoint'
        ),
        Link(
            template=urljoin(base, webfinger),
            type_='application/json', rel='lrdd',
        ),
        Link(
            href=urljoin(base, reverse('wellknowns:manifest')),
            rel='manifest', type_='application/json',
        ),
        Link(href=license, type_='text/html', rel='license'),
        Link(href=license+'rdf', type_='application/rdf+xml', rel='license'),
        Link(href=pkg['repository'], type_='text/html', rel='code-repository'),
    )
    dest.extend(links)


def host_meta(request):
    h = XRD(subject='https://' + request.site.domain)
    add_links(request, h.links)
    return h


def host_meta_xml(request):
    return HttpResponse(
        host_meta(request).to_xml().toprettyxml(indent='  ', encoding='utf-8'),
        content_type='application/xrd+xml',
    )


# The XRD package doesn't actually generate correct JSON, so we have to do it
# ourselves instead.
def host_meta_json(request):
    meta = host_meta(request)
    links = []
    for l in meta.links:
        link = {
            'rel': l.rel, 'type': l.type,
            'href': l.href, 'template': l.template,
        }
        for k in list(link.keys()):
            if not link[k]:
                del link[k]
        links.append(link)

    meta = {'links': links, 'subject': meta.subject}
    return JsonResponse(meta)
