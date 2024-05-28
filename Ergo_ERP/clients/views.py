from django.db.models import Q
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DeleteView

from Ergo_ERP.clients.forms import ClientsModelForm
from Ergo_ERP.clients.models import Clients


class ClientsList(ListView):
    """
    A view for a list of Suppliers instances with multi-field search
    """
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


class ClientsCreate (CreateView):
    model = Clients
    form_class = ClientsModelForm
    template_name = 'clients/clients-create.html'
    extra_context = {'template_verbose_name': 'Create client'}
    success_url = reverse_lazy('clients_list')


class ClientsEdit (UpdateView):
    model = Clients
    form_class = ClientsModelForm
    template_name = 'clients/clients-edit.html'
    extra_context = {'template_verbose_name': 'Edit client'}
    success_url = reverse_lazy('clients_list')


class ClientsDelete (DeleteView):
    model = Clients
    success_url = reverse_lazy('clients_list')
