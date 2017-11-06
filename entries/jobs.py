import requests
from django.conf import settings
from django_rq import job
from ronkyuu import webmention


@job
def ping_hub(*urls):
    data = [('hub.mode', 'publish')] + [('hub.url[]', url) for url in urls]
    requests.post(settings.PUSH_HUB, data=data)


@job
def send_mentions(url):
    result = webmention.findMentions(url)
    for target in result['refs']:
        webmention.sendWebmention(url, target)
