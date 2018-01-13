from debug_toolbar.middleware import show_toolbar as core_show_toolbar


def show_toolbar(request):
    if request.path.endswith('/amp'):
        return False
    return core_show_toolbar(request)
