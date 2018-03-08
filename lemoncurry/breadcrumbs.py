from django.urls import reverse

breadcrumbs = {}


class Crumb:
    def __init__(self, route, label=None, parent=None):
        self.route = route
        self._label = label
        self.parent = parent

    @property
    def label(self):
        return self._label

    def __eq__(self, other):
        if hasattr(other, 'route'):
            return self.route == other.route
        return self.route == other

    def __hash__(self):
        return hash(self.route)

    def __repr__(self):
        return "Crumb('{0}')".format(self.route)

    def use_match(self, match):
        self.match = match

    @property
    def url(self):
        return reverse(self.route)


def add(route, label=None, parent=None):
    if not isinstance(route, Crumb):
        route = Crumb(route, label, parent)
    breadcrumbs[route.route] = route


def find(match):
    crumbs = []
    route = match.view_name
    while route:
        crumb = breadcrumbs[route]
        crumb.use_match(match)
        crumbs.append(crumb)
        route = crumb.parent
    crumbs.reverse()
    return crumbs
