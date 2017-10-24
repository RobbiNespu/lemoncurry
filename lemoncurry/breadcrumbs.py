breadcrumbs = {}


def add(route, label, parent=None):
    breadcrumbs[route] = {'label': label, 'route': route, 'parent': parent}


def find(route):
    crumbs = []
    while route:
        crumb = breadcrumbs[route]
        crumbs.append(crumb)
        route = crumb['parent']
    crumbs.reverse()
    return crumbs
