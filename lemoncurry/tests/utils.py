from unittest.mock import Mock
from .. import utils


class TestOrigin:
    def test_simple_http(self):
        """should return the correct origin for a vanilla HTTP site"""
        req = Mock(scheme='http', site=Mock(domain='lemoncurry.test'))
        assert utils.origin(req) == 'http://lemoncurry.test'

    def test_simple_https(self):
        """should return the correct origin for a vanilla HTTPS site"""
        req = Mock(scheme='https', site=Mock(domain='secure.lemoncurry.test'))
        assert utils.origin(req) == 'https://secure.lemoncurry.test'


class TestUri:
    def test_siteroot(self):
        """should return correct full URI for requests to the site root"""
        req = Mock(scheme='https', path='/', site=Mock(domain='l.test'))
        assert utils.uri(req) == 'https://l.test/'

    def test_path(self):
        """should return correct full URI for requests with a path"""
        req = Mock(scheme='https', path='/notes/23', site=Mock(domain='l.tst'))
        assert utils.uri(req) == 'https://l.tst/notes/23'
