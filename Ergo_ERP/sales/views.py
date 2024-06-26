from django.db import transaction, DatabaseError
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse

from Ergo_ERP.common.helper_functions import is_formset_nonempty, products_list_save_to_document, \
    get_next_document_number
from Ergo_ERP.inventory.helper_functions import check_inventory, update_inventory
from Ergo_ERP.sales.forms import SalesDocumentForm, SoldProductsFormSet, InvoiceDataForm
from Ergo_ERP.sales.models import InvoicedProducts, InvoiceData
from Ergo_ERP.user_settings.models import UserSettings


def products_copy_to_document(
        document_instance,
        products_instances: list,
        fields_to_copy: list,
        products_model_in_which_to_copy,
        name_of_foreignkey_field: str
):
    """
    Creates copies of product form instances from a formset, with specified fields
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
        try:
            copied_product_instance.save()
        except DatabaseError as de:
            raise DatabaseError(f"Database error while saving copied product instance: {de}")
        except Exception as e:
            raise Exception(f"An unexpected error occurred while saving copied product instance: {e}")


def handle_sale_forms(request, sales_document_form, sold_products_formset):
    """
    Handles the SalesDocumentForm instance and the SoldProductsForm instances,
    from the formset, which are linked to it. Updates the Inventory afterwords.
    In that way it creates a Sales document.
    """
    department = sales_document_form.cleaned_data.get('department')
    with transaction.atomic():
        sales_document_instance = sales_document_form.save(commit=False)
        sales_document_instance.operator = request.user
        try:
            sales_document_instance.save()
        except DatabaseError as de:
            raise DatabaseError(f"Database error while saving Sales document instance: {de}")
        except Exception as e:
            raise Exception(f"An unexpected error occurred while saving Sales document instance: {e}")
        sold_product_instances = products_list_save_to_document(
                                    sold_products_formset,
                                    sales_document_instance,
                                    'sales_document_in_which_sold'
                                 )
        update_inventory(sold_product_instances, False, department)
        return sales_document_instance, sold_product_instances


def handle_invoice_forms(sales_document_instance, sold_product_instances, invoice_data_form):
    """
    Handles the InvoiceDataForm instance. Copies the SodProductsForm instances and creates
    InvoicedProductsForm instances, which are linked to InvoiceDataForm. In that way it creates an
    Invoice document based on the Sales document.
    """
    with transaction.atomic():
        fields_to_copy = InvoicedProducts.get_fields_to_copy()
        invoice_document_instance = invoice_data_form.save(commit=False)
        invoice_document_instance.sales_document_for_invoice = sales_document_instance
        invoice_document_instance.save()
        try:
            invoice_document_instance.save()
        except DatabaseError as de:
            raise DatabaseError(f"Database error while saving Invoice document instance: {de}")
        except Exception as e:
            raise Exception(f"An unexpected error occurred while saving Invoice document instance: {e}")
        products_copy_to_document(
            invoice_document_instance,
            sold_product_instances,
            fields_to_copy,
            InvoicedProducts,
            'invoice_document_in_which_included'
        )


def sales_document_create_view(request):
    """
    View function handling a new Sales event in two cases - with or without an invoice
    """
    sold_products_formset = SoldProductsFormSet(request.POST or None, prefix='sold_products')
    user_settings = get_object_or_404(UserSettings, user=request.user)
    if request.method == 'POST':
        sales_document_form = SalesDocumentForm(request.POST)
        invoice_data_form = InvoiceDataForm(request.POST)
        if (
            sales_document_form.is_valid()
            and sold_products_formset.is_valid()
            and is_formset_nonempty(sold_products_formset)
            and check_inventory(sales_document_form, sold_products_formset)
        ):
            if not sales_document_form.cleaned_data['is_linked_to_invoice']:
                handle_sale_forms(request, sales_document_form, sold_products_formset)
                return redirect(reverse('sale_new'))
            elif sales_document_form.cleaned_data['is_linked_to_invoice'] and invoice_data_form.is_valid():
                with transaction.atomic():
                    sales_document_instance, sold_product_instances = handle_sale_forms(request, sales_document_form, sold_products_formset)
                    handle_invoice_forms(sales_document_instance, sold_product_instances, invoice_data_form)
                    return redirect(reverse('sale_new'))
    else:
        sales_document_form = SalesDocumentForm(initial={
            'department': user_settings.default_department,
            'buyer_name': user_settings.default_client,
            'is_linked_to_invoice': user_settings.default_sales_doc_is_invoice
        })
        invoice_data_form = InvoiceDataForm(
            initial={'invoice_number': get_next_document_number(InvoiceData, 'invoice_number')}
        )

    context = {
        'sales_document_form': sales_document_form,
        'sold_products_formset': sold_products_formset,
        'invoice_data_form': invoice_data_form,
        'user_settings': user_settings,
        'template_verbose_name': 'Sale',
    }
    return render(request, 'sales/sale.html', context)


