from django.db.models import Q
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView

from Ergo_ERP.clients.forms import ClientsModelForm
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
            queryset = queryset.filter(
                Q(client_names__icontains=search_query) |
                Q(client_phone_number__icontains=search_query) |
                Q(client_email__icontains=search_query) |
                Q(client_identification_number__icontains=search_query) |
                Q(client_accountable_person__icontains=search_query) |
                Q(client_card_code__icontains=search_query)
            )
        return queryset


class ClientsCreateView (CreateView):
    model = Clients
    form_class = ClientsModelForm
    template_name = 'clients/clients-create.html'
    extra_context = {'template_verbose_name': 'Create client'}

    def get_success_url(self):
        return reverse_lazy('clients_create')

