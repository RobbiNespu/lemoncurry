from annoying.decorators import render_to
from django.shortcuts import get_object_or_404
from users.models import User
from lemoncurry import breadcrumbs, utils

breadcrumbs.add('home:index', 'home')


@render_to('home/index.html')
def index(request):
    query = User.objects.prefetch_related('entries', 'profiles', 'keys')
    user = get_object_or_404(query, pk=1)
    uri = utils.uri(request)

    return {
        'user': user,
        'entries': user.entries.all(),
        'meta': user.as_meta(request),
    }
