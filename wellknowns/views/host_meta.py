from django.http import HttpResponse
from django.urls import reverse
from lemoncurry.utils import load_package_json, origin
from urllib.parse import urljoin
from xrd import XRD, Attribute, Element, Link


def add_links(request, dest):
    base = origin(request)
    package = load_package_json()
    links = (
        Link(rel='lrdd', template=urljoin(base, reverse('wellknowns:webfinger') + '?resource={uri}')),
        Link(rel='license', href='https://creativecommons.org/licenses/by-sa/4.0/'),
        Link(rel='code-repository', href=package['repository']),
    )
    dest.extend(links)


def host_meta(request):
    h = XRD()
    h.attributes.append(Attribute('xmlns:hm', 'http://host-meta.net/ns/1.0'))
    h.elements.append(Element('hm:Host', request.META['HTTP_HOST']))
    add_links(request, h.links)
    return h


def host_meta_xml(request):
    return HttpResponse(
        host_meta(request).to_xml().toprettyxml(indent='  ', encoding='utf-8'),
        content_type='application/xrd+xml',
    )


def host_meta_json(request):
    return HttpResponse(
        host_meta(request).to_json(),
        content_type='application/json'
    )
