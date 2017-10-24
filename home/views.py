from django.shortcuts import get_object_or_404, render
from users.models import User
from lemoncurry import breadcrumbs

breadcrumbs.add('home:index', 'home')


def index(request):
    user = get_object_or_404(User, pk=1)
    return render(request, 'home/index.html', {
        'user': user,
        'meta': user.as_meta(request),
    })
