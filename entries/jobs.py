from django_push import publisher
from django_rq import job


@job
def ping_hub(*urls):
    for url in urls:
        publisher.ping_hub(url)
