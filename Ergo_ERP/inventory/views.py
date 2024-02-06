from django.db import transaction
from django.shortcuts import render, redirect
from django.urls import reverse
from django.views.generic import ListView

from Ergo_ERP.inventory.forms import WarehouseDocumentForm, TransferredProductsFormSet
from Ergo_ERP.inventory.models import Inventory
from Ergo_ERP.products.models import ProductsModel
from Ergo_ERP.sales.views import is_formset_nonempty, products_list_save_to_document


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

def update_inventory(warehouse_document_form, transferred_products_formset):
    products = Inventory.objects.all()
    for product in products:
        if product.product_name == document_product_name and product.product_lot_number == document_product_lot:
            if document_receiving:
                product.product_quantity

def receive_products_dropdown():
    products = ProductsModel.objects.all()
    products_names = []
    for product in products:
        products_names.append(product.product_name)
    return products_names


def handle_receive_document_forms(warehouse_document_form, transferred_products_formset):
    with transaction.atomic():
        warehouse_document_instance = warehouse_document_form.save(commit=False)
        warehouse_document_instance.receiving = True
        warehouse_document_instance.save()
        products_list_save_to_document(
            transferred_products_formset,
            warehouse_document_instance,
            'warehouse_document_in_which_included'
            )


def receiving_document_create(request):
    """
    Handles receiving goods into warehouse and including them in inventory
    """
    warehouse_document_form = WarehouseDocumentForm(request.POST or None)
    transferred_products_formset = TransferredProductsFormSet(request.POST or None, prefix='transferred_products')
    products_dropdown = receive_products_dropdown()

    if request.method == 'POST':
        if (
                warehouse_document_form.is_valid()
                and transferred_products_formset.is_valid()
                and is_formset_nonempty(transferred_products_formset)
        ):
            handle_receive_document_forms(warehouse_document_form, transferred_products_formset)
            return redirect(reverse('receive-goods'))

    context = {
        'warehouse_document_form': warehouse_document_form,
        'transferred_products_formset': transferred_products_formset,
        'products_dropdown': products_dropdown,
    }
    return render(request, 'inventory/receive-goods.html', context)
