from django.core.exceptions import ValidationError
from django.db import transaction
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.views.generic import ListView

from Ergo_ERP.common.helper_functions import is_formset_nonempty, products_list_save_to_document
from Ergo_ERP.common.views import inventory_products_dict
from Ergo_ERP.inventory.forms import ReceivingDocumentForm, ReceivedProductsFormSet, ShippingDocumentForm, \
    ShippedProductsFormSet
from Ergo_ERP.inventory.models import Inventory, Department
from Ergo_ERP.products.models import ProductsModel
from Ergo_ERP.user_settings.models import UserSettings


class InventoryView(ListView):
    """
    A view for the list of inventory items with a filter by Department and search
    """
    model = Inventory
    template_name = 'inventory/inventory.html'
    context_object_name = 'inventory_list'
    extra_context = {'template_verbose_name': 'Inventory'}

    def get_queryset(self):
        queryset = super().get_queryset()
        search_query = self.request.GET.get('search_query') or ''
        department = self.request.GET.get('department') or ''
        if department:
            queryset = queryset.filter(department__name__icontains=department)
        if search_query:
            queryset = queryset.filter(product_name__icontains=search_query)
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['departments'] = Department.objects.all()  # Add the list of departments to the context
        return context


def receive_products_dropdown():
    """
    Returns a simple list pf product names specifically for Warehouse receiving,
    since it is different from other documents.
    """
    products = ProductsModel.objects.all()
    products_names = []
    for product in products:
        products_names.append(product.product_name)
    return products_names


def check_product_name(document_form, products_formset):
    """
    Check if a product name is present in ProductsModel and is therefore a valid entry in the form
    """
    valid_name = True
    for form in products_formset:
        cleaned_data = form.cleaned_data
        product_name = cleaned_data.get('product_name')
        matching_product = ProductsModel.objects.filter(product_name=product_name)
        if product_name and not matching_product.exists():
            form.add_error('product_name', "No such product!")
            valid_name = False
    return valid_name


def create_inventory_instance(product_instance):
    """
    Creates a new instance of in Inventory
    """
    new_inventory_instance = Inventory()
    field_names = [field.name for field in new_inventory_instance._meta.fields if field.name != 'id']
    for field_name in field_names:
        setattr(new_inventory_instance, field_name, getattr(product_instance, field_name))
    new_inventory_instance.save()


# def receive_in_inventory(product_instance):
#

def update_inventory(product_instances, is_receiving: bool, department):
    """
    Adds to and removes from quantities and value of existing products.
    Adjusts current median purchase price.
    Creates new product lots in inventory if necessary.
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
                matching_inventory_instance.product_total += product_instance.product_total
                matching_inventory_instance.purchase_price = (matching_inventory_instance.product_total /
                                                              matching_inventory_instance.product_quantity)
                matching_inventory_instance.save()
            else:
                if matching_inventory_instance.product_quantity < product_instance.product_quantity:
                    raise ValidationError(f"There is not enough of product {matching_inventory_instance.product_name} "
                                          f"with lot {matching_inventory_instance.product_lot_number}.")
                else:
                    matching_inventory_instance.product_quantity -= product_instance.product_quantity
                    matching_inventory_instance.product_total -= (product_instance.product_quantity *
                                                                  matching_inventory_instance.product_purchase_price)
                    matching_inventory_instance.save()
        elif is_receiving:
            create_inventory_instance(product_instance)


def handle_receiving_document_forms(receiving_document_form, received_products_formset):
    """
    Saves receive document form and the product form formset, after setting document as
    linked_warehouse_document for each product in formset. Updates Inventory afterwords
    """
    with transaction.atomic():
        receive_document_instance = receiving_document_form.save(commit=False)
        department = receive_document_instance.receiving_department
        receive_document_instance.save()
        product_instances = products_list_save_to_document(
            received_products_formset,
            receive_document_instance,
            'linked_warehouse_document',
            department
            )
        update_inventory(product_instances, True, department)


def receiving_document_create(request):
    """
    Handles receiving goods into warehouse and adding them to inventory
    """

    received_products_formset = ReceivedProductsFormSet(request.POST or None, prefix='transferred_products')
    products_dropdown = receive_products_dropdown()
    user_settings = get_object_or_404(UserSettings, user=request.user)

    if request.method == 'POST':
        receiving_document_form = ReceivingDocumentForm(request.POST)
        if (
                receiving_document_form.is_valid()
                and received_products_formset.is_valid()
                and is_formset_nonempty(received_products_formset)
                and check_product_name(receiving_document_form, received_products_formset)
        ):
            handle_receiving_document_forms(receiving_document_form, received_products_formset)
            return redirect(reverse('receive-goods'))
    else:
        receiving_document_form = ReceivingDocumentForm(initial={
            'receiving_department': user_settings.default_department}
        )
    context = {
        'receiving_document_form': receiving_document_form,
        'received_products_formset': received_products_formset,
        'products_dropdown': products_dropdown,
        'user_settings': user_settings,
        'template_verbose_name': 'Receiving',
    }
    return render(request, 'inventory/warehouse_receiving.html', context)


def handle_shipping_document_forms(shipping_document_form, shipped_products_formset):
    """
    Saves shipping document form and the product form formset, after setting document as
    linked_warehouse_document for each product in formset. Updates Inventory afterwords
    """
    with transaction.atomic():
        shipping_document_instance = shipping_document_form.save(commit=False)
        department = shipping_document_instance.shipping_department
        shipping_document_instance.save()
        product_instances = products_list_save_to_document(
            shipped_products_formset,
            shipping_document_instance,
            'linked_warehouse_document'
            )
        update_inventory(product_instances, False, department)


def shipping_document_create(request):
    """
    Handles shipping goods from warehouse and removing them from inventory
    """
    shipped_products_formset = ShippedProductsFormSet(request.POST or None, prefix='transferred_products')
    products_dropdown = inventory_products_dict()
    user_settings = get_object_or_404(UserSettings, user=request.user)

    if request.method == 'POST':
        shipping_document_form = ShippingDocumentForm(request.POST)
        if (
                shipping_document_form.is_valid()
                and shipped_products_formset.is_valid()
                and is_formset_nonempty(shipped_products_formset)
        ):
            handle_shipping_document_forms(shipping_document_form, shipped_products_formset)
            return redirect(reverse('ship-goods'))

    else:
        shipping_document_form = ShippingDocumentForm(initial={'shipping_department': user_settings.default_department})
    context = {
        'shipping_document_form': shipping_document_form,
        'shipped_products_formset': shipped_products_formset,
        'products_dropdown': products_dropdown,
        'user_settings': user_settings,
        'template_verbose_name': 'Shipping',
    }
    return render(request, 'inventory/warehouse_shipping.html', context)
