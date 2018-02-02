from collections import namedtuple
import pytest

from .. import breadcrumbs as b


@pytest.fixture
def nested_crumbs():
    x = {'route': 'nc.x', 'label': 'x', 'parent': None}
    y = {'route': 'nc.y', 'label': 'y', 'parent': 'nc.x'}
    z = {'route': 'nc.z', 'label': 'z', 'parent': 'nc.y'}
    crumbs = (x, y, z)

    for crumb in crumbs:
        b.breadcrumbs[crumb['route']] = crumb
    yield namedtuple('NestedCrumbs', 'x y z')(*crumbs)
    for crumb in crumbs:
        del b.breadcrumbs[crumb['route']]


class TestAdd:
    def test_inserts_a_breadcrumb_without_parent(self):
        route = 'tests.add.insert'
        assert route not in b.breadcrumbs
        b.add(route, 'some label')
        assert route in b.breadcrumbs
        assert b.breadcrumbs[route] == {
            'route': route, 'label': 'some label', 'parent': None
        }

    def test_inserts_a_breadcrumb_with_parent(self):
        route = 'tests.add.with_parent'
        parent = 'tests.add.insert'
        assert route not in b.breadcrumbs
        b.add(route, 'child label', parent)
        assert route in b.breadcrumbs
        assert b.breadcrumbs[route] == {
            'route': route, 'label': 'child label', 'parent': parent
        }


class TestFind:
    def test_finds_chain_of_crumbs(self, nested_crumbs):
        crumbs = b.find(nested_crumbs.z['route'])
        assert len(crumbs) == 3
        assert crumbs[0] == nested_crumbs.x
        assert crumbs[1] == nested_crumbs.y
        assert crumbs[2] == nested_crumbs.z
