from django.core.exceptions import ValidationError
from django.db import transaction
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.views.generic import ListView

from Ergo_ERP.common.helper_functions import is_formset_nonempty, products_list_save_to_document, \
    add_department_to_products
from Ergo_ERP.common.views import products_dict_dropdown
from Ergo_ERP.inventory.forms import ReceivingDocumentForm, ReceivedProductsFormSet, ShippingDocumentForm, \
    ShippedProductsFormSet
from Ergo_ERP.inventory.models import Inventory
from Ergo_ERP.products.models import ProductsModel
from Ergo_ERP.user_settings.models import UserSettings


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


def create_inventory_instance(product_instance):
    new_inventory_instance = Inventory()
    field_names = [field.name for field in new_inventory_instance._meta.fields if field.name != 'id']
    for field_name in field_names:
        setattr(new_inventory_instance, field_name, getattr(product_instance, field_name))
    new_inventory_instance.save()


def update_inventory(product_instances, is_receiving: bool, department):
    """
    Adds to and removes from quantities of existing products.
    Creates new products in inventory
    """
    for product_instance in product_instances:
        matching_inventory_instance = Inventory.objects.filter(
            product_name=product_instance.product_name,
            product_lot_number=product_instance.product_lot_number,
            department=department
        ).first()

        if matching_inventory_instance:
            if is_receiving:
                matching_inventory_instance.product_quantity += product_instance.product_quantity
                matching_inventory_instance.save()
            else:
                if matching_inventory_instance.product_quantity < product_instance.product_quantity:
                    raise ValidationError(f"There is not enough of product {matching_inventory_instance.product_name} "
                                          f"with lot {matching_inventory_instance.product_lot_number}.")
                else:
                    matching_inventory_instance.product_quantity -= product_instance.product_quantity
                    matching_inventory_instance.save()
        elif is_receiving:
            create_inventory_instance(product_instance)


def handle_receiving_document_forms(receiving_document_form, received_products_formset):
    with transaction.atomic():
        receive_document_instance = receiving_document_form.save(commit=False)
        department = receive_document_instance.receiving_department
        receive_document_instance.save()
        product_instances = products_list_save_to_document(
            received_products_formset,
            receive_document_instance,
            'linked_warehouse_document'
            )
        product_instances_department = add_department_to_products(product_instances, department)
        update_inventory(product_instances_department, True, department)


def receiving_document_create(request):
    """
    Handles receiving goods into warehouse and adding them to inventory
    """
    receiving_document_form = ReceivingDocumentForm(request.POST or None)
    received_products_formset = ReceivedProductsFormSet(request.POST or None, prefix='transferred_products')
    products_dropdown = receive_products_dropdown()
    user_settings = get_object_or_404(UserSettings, user=request.user)

    if request.method == 'POST':
        if (
                receiving_document_form.is_valid()
                and received_products_formset.is_valid()
                and is_formset_nonempty(received_products_formset)
        ):
            handle_receiving_document_forms(receiving_document_form, received_products_formset)
            return redirect(reverse('receive-goods'))

    context = {
        'receiving_document_form': receiving_document_form,
        'received_products_formset': received_products_formset,
        'products_dropdown': products_dropdown,
        'user_settings': user_settings,
        'template_verbose_name': 'Receiving',
    }
    return render(request, 'inventory/warehouse_receiving.html', context)


def handle_shipping_document_forms(shipping_document_form, shipped_products_formset):
    with transaction.atomic():
        shipping_document_instance = shipping_document_form.save(commit=False)
        department = shipping_document_instance.shipping_department
        shipping_document_instance.save()
        product_instances = products_list_save_to_document(
            shipped_products_formset,
            shipping_document_instance,
            'linked_warehouse_document'
            )
        product_instances_department = add_department_to_products(product_instances, department)
        update_inventory(product_instances_department, True, department)


def shipping_document_create(request):
    """
    Handles shipping goods from warehouse and removing them from inventory
    """
    shipping_document_form = ShippingDocumentForm(request.POST or None)
    shipped_products_formset = ShippedProductsFormSet(request.POST or None, prefix='transferred_products')
    products_dropdown = products_dict_dropdown()
    user_settings = get_object_or_404(UserSettings, user=request.user)

    if request.method == 'POST':
        if (
                shipping_document_form.is_valid()
                and shipped_products_formset.is_valid()
                and is_formset_nonempty(shipped_products_formset)
        ):
            handle_shipping_document_forms(shipping_document_form, shipped_products_formset)
            return redirect(reverse('ship-goods'))

    context = {
        'shipping_document_form': shipping_document_form,
        'shipped_products_formset': shipped_products_formset,
        'products_dropdown': products_dropdown,
        'user_settings': user_settings,
        'template_verbose_name': 'Shipping',
    }
    return render(request, 'inventory/warehouse_shipping.html', context)
