from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView
from typing import Dict, Optional, Set
from lemoncurry.requests import mf2


class ClientsDict(dict):
    def __missing__(self, client_id):
        self[client_id] = Client(client_id)
        return self[client_id]


class Client:
    id: str
    count: int
    scopes: Set[str]
    app: Optional[Dict[str, str]]

    def __init__(self, client_id):
        self.id = client_id
        self.count = 0
        self.scopes = set()
        apps = mf2(self.id).to_dict(filter_by_type='h-x-app')
        try:
            self.app = apps[0]['properties']
        except IndexError:
            self.app = None


class TokensListView(LoginRequiredMixin, TemplateView):
    template_name = 'lemonauth/tokens.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        clients = ClientsDict()
        for token in self.request.user.token_set.all():
            client = clients[token.client_id]
            client.count += 1
            client.scopes |= set(token.scope.split(' '))
        context.update({'clients': clients, 'title': 'tokens'})
        return context
