import requests
from django.conf import settings
from django_rq import job
from urllib.parse import urlencode


@job
def ping_hub(*urls):
    requests.post(settings.PUSH_HUB, data={
        'hub.mode': 'publish',
        'hub.url': ','.join(map(urlencode, urls)),
    })
