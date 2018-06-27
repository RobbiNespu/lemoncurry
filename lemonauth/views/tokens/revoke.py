from django.http import HttpResponse
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views import View


class TokensRevokeView(LoginRequiredMixin, View):
    def delete(self, request, client_id: str):
        request.user.token_set.filter(client_id=client_id).delete()
        return HttpResponse(status=204)
