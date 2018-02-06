from ...views import static


def test_redirect_to_static(rf):
    res = static.redirect_to_static('abcd')(rf.get('/'))
    assert res.status_code == 302
    assert res.url == '/static/wellknowns/abcd'


def test_keybase(rf):
    res = static.keybase(rf.get('/.well-knowns/keybase.txt'))
    assert res.status_code == 302
    assert res.url == '/static/wellknowns/keybase.txt'
