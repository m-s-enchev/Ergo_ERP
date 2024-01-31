from django.shortcuts import render
from django.views.generic import ListView

from Ergo_ERP.inventory.models import Inventory


class InventoryView(ListView):
    model = Inventory
    template_name = 'inventory/inventory.html'
    context_object_name = 'inventory_list'

    def get_queryset(self):
        queryset = super().get_queryset()
        search_query = self.request.GET.get('search_query') or ''
        if search_query:
            queryset = queryset.filter(product_name__icontains=search_query)
        return queryset

