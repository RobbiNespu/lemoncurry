from django.views.generic.base import RedirectView
from django.contrib.staticfiles.templatetags.staticfiles import static


def redirect_to_static(file):
    return RedirectView.as_view(url=static('wellknowns/' + file))


keybase = redirect_to_static('keybase.txt')
