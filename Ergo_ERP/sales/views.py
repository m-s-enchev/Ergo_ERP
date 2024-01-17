from django.db import transaction
from django.shortcuts import render, redirect
from django.urls import reverse

from Ergo_ERP.sales.forms import SalesDocumentForm, SoldProductsFormSet, InvoiceDataForm
from Ergo_ERP.sales.models import InvoicedProducts


def at_least_one_form_in_formset_not_empty(formset):
    for form in formset:
        if form.cleaned_data:
            return True
    return False


def sold_products_save(sold_products_formset, sales_document_instance):
    saved_product_instances = []
    for sold_products_form in sold_products_formset:
        if sold_products_form.cleaned_data:
            sold_products_instance = sold_products_form.save(commit=False)
            sold_products_instance.sales_document_in_which_sold = sales_document_instance
            sold_products_instance.save()
            saved_product_instances.append(sold_products_instance)
    return saved_product_instances


def invoice_data_save(invoice_data_form, sales_document_instance, sold_products_instances: list):
    invoice_data_instance = invoice_data_form.save(commit=False)
    invoice_data_instance.sales_document_for_invoice = sales_document_instance
    invoice_data_instance.save()
    for product_instance in sold_products_instances:
        invoiced_product_instance = InvoicedProducts()
        for field in product_instance._meta.fields:
            if field.name != 'id' and field.name != 'sales_document_in_which_sold':
                setattr(invoiced_product_instance, field.name, getattr(product_instance, field.name))
        invoiced_product_instance.invoice_document_in_which_included = invoice_data_instance
        invoiced_product_instance.save()


def sales_document(request):
    sales_document_form = SalesDocumentForm(request.POST or None)
    sold_products_formset = SoldProductsFormSet(request.POST or None, prefix='sold_products')
    invoice_data_form = InvoiceDataForm(request.POST or None)

    if request.method == 'POST':
        if (
            sales_document_form.is_valid()
            and sold_products_formset.is_valid()
            and at_least_one_form_in_formset_not_empty(sold_products_formset)
        ):
            if not sales_document_form.cleaned_data['is_linked_to_invoice']:
                with transaction.atomic():
                    sales_document_instance = sales_document_form.save()
                    sold_products_save(sold_products_formset, sales_document_instance)
                return redirect(reverse('sale_new'))
            elif sales_document_form.cleaned_data['is_linked_to_invoice'] and invoice_data_form.is_valid():
                with transaction.atomic():
                    sales_document_instance = sales_document_form.save()
                    sold_product_instances = sold_products_save(sold_products_formset, sales_document_instance)
                    invoice_data_save(invoice_data_form, sales_document_instance, sold_product_instances)
                return redirect(reverse('sale_new'))

    context = {
        'sales_document_form': sales_document_form,
        'sold_products_formset': sold_products_formset,
        'invoice_data_form': invoice_data_form
    }
    return render(request, 'sales/sale.html', context)



################################               OLD      #################################################



#
# def at_least_one_form_in_formset_not_empty(formset):
#     for form in formset:
#         if form.cleaned_data:
#             return True
#     return False
#
#
# def sold_products_save(sold_products_formset, sales_document_instance):
#     for sold_products_form in sold_products_formset:
#         if sold_products_form.cleaned_data:
#             sold_products_instance = sold_products_form.save(commit=False)
#             sold_products_instance.sales_document_in_which_sold = sales_document_instance
#             sold_products_instance.save()
#
#
# def invoice_data_save(invoice_data_form, sales_document_instance, sold_products_formset):
#     invoice_data_instance = invoice_data_form.save(commit=False)
#     invoice_data_instance.sales_document_for_invoice = sales_document_instance
#     invoice_data_instance.save()
#     for sold_products_form in sold_products_formset:
#         if sold_products_form.cleaned_data:
#             sold_products_instance = sold_products_form.save(commit=False)
#             sold_products_instance.sales_document_in_which_sold = sales_document_instance
#             sold_products_instance.save()
#             invoiced_product_instance = InvoicedProducts()
#             for field in sold_products_instance._meta.fields:
#                 if field.name != 'id' and field.name != 'sales_document_in_which_sold':
#                     setattr(invoiced_product_instance, field.name, getattr(sold_products_instance, field.name))
#             invoiced_product_instance.invoice_document_in_which_included = invoice_data_instance
#             invoiced_product_instance.save()
#
#
# def sales_document(request):
#     sales_document_form = SalesDocumentForm(request.POST or None)
#     sold_products_formset = SoldProductsFormSet(request.POST or None, prefix='sold_products')
#     invoice_data_form = InvoiceDataForm(request.POST or None)
#
#     if request.method == 'POST':
#         if (
#             sales_document_form.is_valid()
#             and sold_products_formset.is_valid()
#             and at_least_one_form_in_formset_not_empty(sold_products_formset)
#         ):
#             if not sales_document_form.cleaned_data['is_linked_to_invoice']:
#                 with transaction.atomic():
#                     sales_document_instance = sales_document_form.save()
#                     sold_products_save(sold_products_formset, sales_document_instance)
#                 return redirect(reverse('sale_new'))
#             elif sales_document_form.cleaned_data['is_linked_to_invoice'] and invoice_data_form.is_valid():
#                 with transaction.atomic():
#                     sales_document_instance = sales_document_form.save()
#                     # sold_products_save(sold_products_formset, sales_document_instance)
#                     invoice_data_save(invoice_data_form, sales_document_instance, sold_products_formset)
#                 return redirect(reverse('sale_new'))
#
#     context = {
#         'sales_document_form': sales_document_form,
#         'sold_products_formset': sold_products_formset,
#         'invoice_data_form': invoice_data_form
#     }
#     return render(request, 'sales/sale.html', context)
