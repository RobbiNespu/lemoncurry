import json
from lxml import etree
import pytest


@pytest.mark.django_db
def test_host_meta_json(client):
    res = client.get('/.well-known/host-meta.json')
    assert res.status_code == 200
    assert res['Content-Type'] == 'application/json'
    meta = json.loads(res.content)
    assert meta.keys() == {'links', 'subject'}
    assert meta['subject'] == 'https://example.com'
    assert len(meta['links']) == 13


@pytest.mark.django_db
def test_host_meta_xml(client):
    res = client.get('/.well-known/host-meta')
    assert res.status_code == 200
    assert res['Content-Type'] == 'application/xrd+xml'
    root = etree.XML(res.content)
    ns = '{http://docs.oasis-open.org/ns/xri/xrd-1.0}'
    assert root.tag == (ns + 'XRD')
    assert root.findtext(ns + 'Subject') == 'https://example.com'
    assert len(root.findall(ns + 'Link')) == 13
