from django.apps import apps
from django.shortcuts import get_object_or_404, redirect

from .convert import abc_to_id


def unshort(request, model, tiny):
    entity = get_object_or_404(apps.get_model(model), pk=abc_to_id(tiny))
    return redirect(entity, permanent=True)
