import pytest


@pytest.mark.django_db
def test_atom(client):
    res = client.get('/atom')
    assert res.status_code == 200
    assert res['Content-Type'] == 'application/atom+xml; charset=utf-8'


@pytest.mark.django_db
def test_rss(client):
    res = client.get('/rss')
    assert res.status_code == 200
    assert res['Content-Type'] == 'application/rss+xml; charset=utf-8'


@pytest.mark.django_db
def test_atom_by_kind(client):
    res = client.get('/notes/atom')
    assert res.status_code == 200
    assert res['Content-Type'] == 'application/atom+xml; charset=utf-8'


@pytest.mark.django_db
def test_rss_by_kind(client):
    res = client.get('/notes/rss')
    assert res.status_code == 200
    assert res['Content-Type'] == 'application/rss+xml; charset=utf-8'
