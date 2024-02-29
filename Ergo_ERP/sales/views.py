import datetime

from django.db import transaction
from django.db.models import Max
from django.shortcuts import render, redirect
from django.urls import reverse

from Ergo_ERP.common.helper_functions import is_formset_nonempty, products_list_save_to_document
from Ergo_ERP.inventory.models import Inventory
from Ergo_ERP.inventory.views import update_inventory
from Ergo_ERP.sales.forms import SalesDocumentForm, SoldProductsFormSet, InvoiceDataForm
from Ergo_ERP.sales.models import InvoicedProducts, InvoiceData


def products_copy_to_document(
        document_instance,
        products_instances: list,
        fields_to_copy: list,
        products_model_in_which_to_copy,
        name_of_foreignkey_field: str
):
    """
    Creates copies of product instances, with specified fields
    and associates them to a specified document model instance.
    """
    field_names = [
        field.name
        for field in products_model_in_which_to_copy._meta.fields
        if field.name in fields_to_copy
    ]
    for products_instance in products_instances:
        copied_product_instance = products_model_in_which_to_copy()
        for field_name in field_names:
            setattr(copied_product_instance, field_name, getattr(products_instance, field_name))
        setattr(copied_product_instance, name_of_foreignkey_field, document_instance)
        copied_product_instance.save()


def handle_sales_document_form_only(sales_document_form, sold_products_formset):
    with transaction.atomic():
        sales_document_instance = sales_document_form.save()
        sold_product_instances = products_list_save_to_document(
                                    sold_products_formset,
                                    sales_document_instance,
                                    'sales_document_in_which_sold'
                                 )
        update_inventory(sold_product_instances, False)


def handle_sales_and_invoice_forms(sales_document_form, sold_products_formset, invoice_data_form):
    """
    A separate InvoiceData instance with linked InvoicedProducts instances are created,
    since the date and included products might be different from sales_document instance
    """
    with transaction.atomic():
        sales_document_instance = sales_document_form.save()
        sold_product_instances = products_list_save_to_document(
                                    sold_products_formset,
                                    sales_document_instance,
                                    'sales_document_in_which_sold'
                                 )
        update_inventory(sold_product_instances, False)
        fields_to_copy = InvoicedProducts.get_fields_to_copy()
        invoice_document_instance = invoice_data_form.save(commit=False)
        invoice_document_instance.sales_document_for_invoice = sales_document_instance
        invoice_document_instance.save()
        products_copy_to_document(
            invoice_document_instance,
            sold_product_instances,
            fields_to_copy,
            InvoicedProducts,
            'invoice_document_in_which_included'
        )


def products_dict_dropdown():
    products = Inventory.objects.all()
    products_dict = {}
    for product in products:
        if product.product_exp_date:
            exp_date_formatted = product.product_exp_date.strftime('%d.%m.%Y')
            lot_number = product.product_lot_number
        else:
            exp_date_formatted = ""
            lot_number = ""
        products_dict[product.product_name] = [
                                                format(product.product_quantity.normalize(), 'f'),
                                                lot_number,
                                                exp_date_formatted
                                                ]
    return products_dict


def get_invoice_number():
    last_number = InvoiceData.objects.aggregate(Max('invoice_number'))['invoice_number__max']
    if last_number is None:
        invoice_number = 1
    else:
        invoice_number = last_number + 1
    return invoice_number


def sales_document_create(request):
    """
    View function handling a new sales event in two cases - with or without an invoice
    """
    sales_document_form = SalesDocumentForm(request.POST or None)
    sold_products_formset = SoldProductsFormSet(request.POST or None, prefix='sold_products')
    products_dropdown = products_dict_dropdown()

    if request.method == 'POST':
        invoice_data_form = InvoiceDataForm(request.POST)
        if (
            sales_document_form.is_valid()
            and sold_products_formset.is_valid()
            and is_formset_nonempty(sold_products_formset)
        ):
            if not sales_document_form.cleaned_data['is_linked_to_invoice']:
                handle_sales_document_form_only(sales_document_form, sold_products_formset)
                return redirect(reverse('sale_new'))
            elif sales_document_form.cleaned_data['is_linked_to_invoice'] and invoice_data_form.is_valid():
                handle_sales_and_invoice_forms(sales_document_form, sold_products_formset, invoice_data_form)
                return redirect(reverse('sale_new'))
    else:
        invoice_data_form = InvoiceDataForm(initial={'invoice_number': get_invoice_number()})

    context = {
        'sales_document_form': sales_document_form,
        'sold_products_formset': sold_products_formset,
        'invoice_data_form': invoice_data_form,
        'products_dropdown': products_dropdown,
    }
    return render(request, 'sales/sale.html', context)


