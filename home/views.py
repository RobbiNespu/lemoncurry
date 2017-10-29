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
    person = {
        '@context': 'http://schema.org',
        '@type': 'Person',
        '@id': uri,
        'url': uri,
        'name': '{0} {1}'.format(user.first_name, user.last_name),
        'email': user.email,
        'image': user.avatar.url,
        'givenName': user.first_name,
        'familyName': user.last_name,
        'sameAs': [profile.url for profile in user.profiles.all()]
    }

    return {
        'user': user,
        'person': person,
        'entries': user.entries.all(),
        'meta': user.as_meta(request),
    }
