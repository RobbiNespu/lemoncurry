from django.shortcuts import get_object_or_404, render
from users.models import User
from lemoncurry import breadcrumbs

breadcrumbs.add('home:index', 'home')


def index(request):
    query = User.objects.prefetch_related('entries', 'profiles', 'keys')
    user = get_object_or_404(query, pk=1)
    entries = user.entries.all()
    return render(request, 'home/index.html', {
        'user': user,
        'entries': entries,
        'meta': user.as_meta(request),
    })
