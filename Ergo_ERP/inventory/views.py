from django.shortcuts import render
from django.views.generic import ListView

from Ergo_ERP.inventory.models import Inventory


class InventoryView(ListView):
    model = Inventory
    template_name = 'inventory/inventory.html'
    context_object_name = 'inventory_list'

