from django.shortcuts import get_object_or_404, render
from users.models import User
from lemoncurry import breadcrumbs
from lemoncurry.templatetags.lemoncurry_tags import request_uri

breadcrumbs.add('home:index', 'home')


def index(request):
    query = User.objects.prefetch_related('entries', 'profiles', 'keys')
    user = get_object_or_404(query, pk=1)
    uri = request_uri(request)
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

    entries = user.entries.all()
    return render(request, 'home/index.html', {
        'user': user,
        'person': person,
        'entries': entries,
        'meta': user.as_meta(request),
    })
