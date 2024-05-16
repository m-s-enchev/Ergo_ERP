from django.db.models import Q
from django.shortcuts import render
from django.views.generic import ListView

from Ergo_ERP.suppliers.models import Suppliers


class SuppliersList(ListView):
    model = Suppliers
    template_name = 'suppliers/suppliers-list.html'
    context_object_name = 'suppliers_list'
    extra_context = {'template_verbose_name': 'Suppliers'}

    def get_queryset(self):
        queryset = super().get_queryset()
        search_query = self.request.GET.get('search_query') or ''
        if search_query:
            queryset = queryset.filter(
                Q(supplier_name__icontains=search_query) |
                Q(supplier_phone_number__icontains=search_query) |
                Q(supplier_email__icontains=search_query) |
                Q(supplier_identification_number__icontains=search_query) |
                Q(supplier_accountable_person__icontains=search_query)
            )
        return queryset
