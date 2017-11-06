import requests
from django.conf import settings
from django_rq import job


@job
def ping_hub(*urls):
    requests.post(settings.PUSH_HUB, data={
        'hub.mode': 'publish',
        'hub.url': ','.join(urls),
    })
