from django.http import HttpResponse
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views import View

from ...models import Token


class TokensRevokeView(LoginRequiredMixin, View):
    def delete(self, request, client_id: str):
        Token.objects.filter(client_id=client_id).delete()
        return HttpResponse(status=204)
