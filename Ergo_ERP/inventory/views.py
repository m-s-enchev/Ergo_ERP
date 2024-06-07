from django.db import transaction, DatabaseError
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.views.generic import ListView

from Ergo_ERP.common.helper_functions import is_formset_nonempty, products_list_save_to_document, check_product_name, \
    two_column_products_dict
from Ergo_ERP.common.views import inventory_products_dict
from Ergo_ERP.inventory.forms import ReceivingDocumentForm, ReceivedProductsFormSet, ShippingDocumentForm, \
    ShippedProductsFormSet
from Ergo_ERP.inventory.helper_functions import check_inventory, update_inventory
from Ergo_ERP.inventory.models import Inventory, Department
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
        context['departments'] = Department.objects.all()
        return context


def handle_receiving_document_forms(request, receiving_document_form, received_products_formset):
    """
    Saves receive document form and the product form formset, after setting document as
    linked_warehouse_document for each product in formset. Updates Inventory afterwords
    """
    with transaction.atomic():
        receive_document_instance = receiving_document_form.save(commit=False)
        department = receive_document_instance.receiving_department
        receive_document_instance.operator = request.user
        try:
            receive_document_instance.save()
        except DatabaseError as de:
            raise DatabaseError(f"Database error while saving Warehouse Receive document instance: {de}")
        except Exception as e:
            raise Exception(f"An unexpected error occurred while saving Warehouse Receive document instance: {e}")
        product_instances = products_list_save_to_document(
            received_products_formset,
            receive_document_instance,
            'linked_warehouse_document',
            department
            )
        update_inventory(product_instances, True, department)


def receiving_document_create_view(request):
    """
    View for receiving goods into warehouse and adding them to inventory
    """

    received_products_formset = ReceivedProductsFormSet(request.POST or None, prefix='transferred_products')
    products_dropdown = two_column_products_dict()
    user_settings = get_object_or_404(UserSettings, user=request.user)

    if request.method == 'POST':
        receiving_document_form = ReceivingDocumentForm(request.POST)
        if (
                receiving_document_form.is_valid()
                and received_products_formset.is_valid()
                and is_formset_nonempty(received_products_formset)
                and check_product_name(receiving_document_form, received_products_formset)
        ):
            handle_receiving_document_forms(request, receiving_document_form, received_products_formset)
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


def handle_shipping_document_forms(request, shipping_document_form, shipped_products_formset):
    """
    Saves shipping document form and the product form formset, after setting document as
    linked_warehouse_document for each product in formset. Updates Inventory afterwords
    """
    with transaction.atomic():
        shipping_document_instance = shipping_document_form.save(commit=False)
        department = shipping_document_instance.shipping_department
        shipping_document_instance.operator = request.user
        try:
            shipping_document_instance.save()
        except DatabaseError as de:
            raise DatabaseError(f"Database error while saving Warehouse Shipping document instance: {de}")
        except Exception as e:
            raise Exception(f"An unexpected error occurred while saving Warehouse Shipping document instance: {e}")
        product_instances = products_list_save_to_document(
            shipped_products_formset,
            shipping_document_instance,
            'linked_warehouse_document',
            department
            )
        update_inventory(product_instances, False, department)


def shipping_document_create_view(request):
    """
    View for shipping/selling goods from warehouse and removing them from inventory
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
                and check_inventory(shipping_document_form, shipped_products_formset)
        ):
            handle_shipping_document_forms(request, shipping_document_form, shipped_products_formset)
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
