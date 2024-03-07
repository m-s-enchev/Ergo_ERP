import datetime

from django.db import transaction
from django.shortcuts import render, redirect
from django.urls import reverse

from Ergo_ERP.common.helper_functions import is_formset_nonempty, products_list_save_to_document, \
    get_next_document_number, add_department_to_products
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
        sales_document_instance = sales_document_form.save(commit=False)
        department = sales_document_instance.department
        sales_document_instance.save()
        sold_product_instances = products_list_save_to_document(
                                    sold_products_formset,
                                    sales_document_instance,
                                    'sales_document_in_which_sold'
                                 )
        sold_product_instances_department = add_department_to_products(sold_product_instances, department)
        update_inventory(sold_product_instances_department, False)


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


def check_inventory(sales_document_form, sold_products_formset):
    all_valid = True
    department = sales_document_form.cleaned_data.get('department')
    for form in sold_products_formset:
        cleaned_data = form.cleaned_data
        product_name = cleaned_data.get('product_name')
        product_lot_number = cleaned_data.get('product_lot_number')
        product_quantity = cleaned_data.get('product_quantity')
        matching_inventory = Inventory.objects.filter(
            product_name=product_name,
            product_lot_number=product_lot_number,
            department=department
        )
        if matching_inventory.exists():
            matching_instance = matching_inventory.first()
            if matching_instance.product_quantity < product_quantity:
                form.add_error('product_quantity', "Insufficient quantity")
                all_valid = False
        else:
            form.add_error('product_name', "No such product")
            all_valid = False
        return all_valid


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
            and check_inventory(sales_document_form, sold_products_formset)
        ):
            if not sales_document_form.cleaned_data['is_linked_to_invoice']:
                handle_sales_document_form_only(sales_document_form, sold_products_formset)
                return redirect(reverse('sale_new'))
            elif sales_document_form.cleaned_data['is_linked_to_invoice'] and invoice_data_form.is_valid():
                handle_sales_and_invoice_forms(sales_document_form, sold_products_formset, invoice_data_form)
                return redirect(reverse('sale_new'))
    else:
        invoice_data_form = InvoiceDataForm(
            initial={'invoice_number': get_next_document_number(InvoiceData, 'invoice_number')}
        )

    context = {
        'sales_document_form': sales_document_form,
        'sold_products_formset': sold_products_formset,
        'invoice_data_form': invoice_data_form,
        'products_dropdown': products_dropdown,
        'template_verbose_name': 'Sale',
    }
    return render(request, 'sales/sale.html', context)


