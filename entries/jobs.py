import requests
from django.conf import settings
from django_rq import job


@job
def ping_hub(*urls):
    data = [('hub.mode', 'publish')] + [('hub.url[]', url) for url in urls]
    requests.post(settings.PUSH_HUB, data=data)
