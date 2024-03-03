from django.core.exceptions import ValidationError
from django.db import transaction
from django.db.models import F
from django.shortcuts import render, redirect
from django.urls import reverse
from django.views.generic import ListView

from Ergo_ERP.common.helper_functions import is_formset_nonempty, products_list_save_to_document
from Ergo_ERP.inventory.forms import WarehouseDocumentForm, TransferredProductsFormSet
from Ergo_ERP.inventory.models import Inventory
from Ergo_ERP.products.models import ProductsModel


class InventoryView(ListView):
    model = Inventory
    template_name = 'inventory/inventory.html'
    context_object_name = 'inventory_list'
    extra_context = {'template_verbose_name': 'Inventory'}

    def get_queryset(self):
        queryset = super().get_queryset()
        search_query = self.request.GET.get('search_query') or ''
        if search_query:
            queryset = queryset.filter(product_name__icontains=search_query)
        return queryset


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
        product_instances = products_list_save_to_document(
            transferred_products_formset,
            warehouse_document_instance,
            'warehouse_document_in_which_included'
            )
        return product_instances, warehouse_document_instance.receiving


def create_inventory_instance(product_instance):
    new_inventory_instance = Inventory()
    field_names = [field.name for field in new_inventory_instance._meta.fields if field.name != 'id']
    for field_name in field_names:
        setattr(new_inventory_instance, field_name, getattr(product_instance, field_name))
    new_inventory_instance.save()


def update_inventory(product_instances, is_receiving):
    for product_instance in product_instances:
        matching_inventory = Inventory.objects.filter(
            product_name=product_instance.product_name,
            product_lot_number=product_instance.product_lot_number
        )
        if matching_inventory.exists():
            if is_receiving:
                matching_inventory.update(product_quantity=F('product_quantity') + product_instance.product_quantity)
            else:
                for inv_instance in matching_inventory:
                    new_quantity = inv_instance.product_quantity - product_instance.product_quantity
                    if new_quantity < 0:
                        raise ValidationError(f"There is not enough of product {inv_instance.product_name} "
                                              f"with lot {inv_instance.product_lot_number}.")
                    else:
                        inv_instance.product_quantity = new_quantity
                        inv_instance.save()
        else:
            create_inventory_instance(product_instance)


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
            [product_instances, is_receiving] = handle_receive_document_forms(warehouse_document_form, transferred_products_formset)
            update_inventory(product_instances, is_receiving)
            return redirect(reverse('receive-goods'))

    context = {
        'warehouse_document_form': warehouse_document_form,
        'transferred_products_formset': transferred_products_formset,
        'products_dropdown': products_dropdown,
        'template_verbose_name': 'Receiving',
    }
    return render(request, 'inventory/receive-goods.html', context)
