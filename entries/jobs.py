import requests
from django.conf import settings
from django_rq import job
from ronkyuu import webmention


@job
def ping_hub(*urls):
    for url in urls:
        requests.post(settings.PUSH_HUB, data={
            'hub.mode': 'publish',
            'hub.url': url,
        })


@job
def send_mentions(source):
    result = webmention.findMentions(source)
    for target in result['refs']:
        status, endpoint = webmention.discoverEndpoint(target)
        if endpoint is not None and status == 200:
            webmention.sendWebmention(source, target, endpoint)
