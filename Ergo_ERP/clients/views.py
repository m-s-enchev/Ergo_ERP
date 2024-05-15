from django.shortcuts import render
from django.views.generic import ListView

from Ergo_ERP.clients.models import Clients


# Create your views here.
class ClientsList(ListView):
    model = Clients
    template_name = 'clients/clients-list.html'
    context_object_name = 'clients_list'
    extra_context = {'template_verbose_name': 'Clients'}

    def get_queryset(self):
        queryset = super().get_queryset()
        search_query = self.request.GET.get('search_query') or ''
        if search_query:
            queryset = queryset.filter(client_names__icontains=search_query)
        return queryset

