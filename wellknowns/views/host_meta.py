from django.http import HttpResponse
from django.conf import settings
from lemoncurry.templatetags.lemoncurry_tags import get_package_json
from xrd import XRD, Attribute, Element, Link


def add_links(dest):
    package = get_package_json()
    links = (
        Link(rel='license', href='https://creativecommons.org/licenses/by-sa/4.0/'),
        Link(rel='code-repository', href=package['repository']),
    )
    dest.extend(links)


def host_meta(request):
    h = XRD()
    h.attributes.append(Attribute('xmlns:hm', 'http://host-meta.net/ns/1.0'))
    h.elements.append(Element('hm:Host', request.META['HTTP_HOST']))
    add_links(h.links)
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
