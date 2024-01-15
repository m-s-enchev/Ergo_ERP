from django.db import transaction
from django.shortcuts import render, redirect
from django.urls import reverse

from Ergo_ERP.sales.forms import SalesDocumentForm, SoldProductsFormSet, InvoiceDataFormSet, InvoiceDataForm
from Ergo_ERP.sales.models import InvoicedProducts


def sold_products_save(sold_products_formset, sales_document_instance):
    for sold_products_form in sold_products_formset:
        if sold_products_form.cleaned_data:
            sold_products_instance = sold_products_form.save(commit=False)
            sold_products_instance.sales_document_in_which_sold = sales_document_instance
            sold_products_instance.save()


def invoice_data_save(invoice_data_form, sales_document_instance, sold_products_formset):
    invoice_data_instance = invoice_data_form.save(commit=False)
    invoice_data_instance.sales_document_for_invoice = sales_document_instance
    invoice_data_instance.save()
    for sold_products_form in sold_products_formset:
        if sold_products_form.cleaned_data:
            sold_products_instance = sold_products_form.save(commit=False)
            sold_products_instance.sales_document_in_which_sold = sales_document_instance
            sold_products_instance.save()
            invoiced_product_instance = InvoicedProducts()
            for field in sold_products_instance._meta.fields:
                if field.name != 'id' and field.name != 'sales_document_in_which_sold':
                    setattr(invoiced_product_instance, field.name, getattr(sold_products_instance, field.name))
            invoiced_product_instance.invoice_document_in_which_included = invoice_data_instance
            invoiced_product_instance.save()


def sales_document(request):
    sales_document_form = SalesDocumentForm(request.POST or None)
    sold_products_formset = SoldProductsFormSet(request.POST or None, prefix='sold_products')
    invoice_data_form = InvoiceDataForm(request.POST or None)

    if request.method == 'POST':
        if sales_document_form.is_valid() and sold_products_formset.is_valid():
            if not sales_document_form.cleaned_data['is_linked_to_invoice']:
                with transaction.atomic():
                    sales_document_instance = sales_document_form.save()
                    sold_products_save(sold_products_formset, sales_document_instance)
                return redirect(reverse('sale_new'))
            elif sales_document_form.cleaned_data['is_linked_to_invoice'] and invoice_data_form.is_valid():
                with transaction.atomic():
                    sales_document_instance = sales_document_form.save()
                    sold_products_save(sold_products_formset, sales_document_instance)
                    invoice_data_save(invoice_data_form, sales_document_instance, sold_products_formset)
                return redirect(reverse('sale_new'))

    context = {
        'sales_document_form': sales_document_form,
        'sold_products_formset': sold_products_formset,
        'invoice_data_form': invoice_data_form
    }
    return render(request, 'sales/sale.html', context)




######################################################### invoice and sales are in formset - unnnecessary formset#############

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
#     invoice_data_formset = InvoiceDataFormSet(request.POST or None, prefix='invoice_data')
#
#     if request.method == 'POST':
#         if sales_document_form.is_valid() and sold_products_formset.is_valid():
#             if not sales_document_form.cleaned_data['is_linked_to_invoice']:
#                 with transaction.atomic():
#                     sales_document_instance = sales_document_form.save()
#                     sold_products_save(sold_products_formset, sales_document_instance)
#                 return redirect(reverse('sale_new'))
#             elif sales_document_form.cleaned_data['is_linked_to_invoice'] and invoice_data_formset.is_valid():
#                 with transaction.atomic():
#                     sales_document_instance = sales_document_form.save()
#                     sold_products_save(sold_products_formset, sales_document_instance)
#                     invoice_data_save(invoice_data_formset.forms[0], sales_document_instance, sold_products_formset)
#                 return redirect(reverse('sale_new'))
#
#     context = {
#         'sales_document_form': sales_document_form,
#         'sold_products_formset': sold_products_formset,
#         'invoice_data_formset': invoice_data_formset,
#     }
#     return render(request, 'sales/sale.html', context)


###########################################################   THE OLDER - no invoiced products       #########################################################



# def sold_products_save(sold_products_formset, sales_document_instance):
#     for sold_products_form in sold_products_formset:
#         if sold_products_form.cleaned_data:
#             sold_products_instance = sold_products_form.save(commit=False)
#             sold_products_instance.sales_document_in_which_sold = sales_document_instance
#             sold_products_instance.save()



# def invoice_data_save(invoice_data_formset, sales_document_instance):
#     for invoice_data_form in invoice_data_formset:
#         if invoice_data_form.cleaned_data:
#             invoice_data_instance = invoice_data_form.save(commit=False)
#             invoice_data_instance.sales_document_for_invoice = sales_document_instance
#             invoice_data_instance.save()


# def sales_document(request):
#     sales_document_form = SalesDocumentForm(request.POST or None)
#     sold_products_formset = SoldProductsFormSet(request.POST or None, prefix='sold_products')
#     invoice_data_formset = InvoiceDataFormSet(request.POST or None, prefix='invoice_data')
#
#     if request.method == 'POST':
#         if sales_document_form.is_valid() and sold_products_formset.is_valid():
#             if not sales_document_form.cleaned_data['is_linked_to_invoice']:
#                 with transaction.atomic():
#                     sales_document_instance = sales_document_form.save()
#                     sold_products_save(sold_products_formset, sales_document_instance)
#                 return redirect(reverse('sale_new'))
#
#             elif sales_document_form.cleaned_data['is_linked_to_invoice'] and invoice_data_formset.is_valid():
#                 with transaction.atomic():
#                     sales_document_instance = sales_document_form.save()
#                     sold_products_save(sold_products_formset, sales_document_instance)
#                     invoice_data_save(invoice_data_formset, sales_document_instance)
#                 return redirect(reverse('sale_new'))
#
#     context = {
#         'sales_document_form': sales_document_form,
#         'sold_products_formset': sold_products_formset,
#         'invoice_data_formset': invoice_data_formset,
#     }
#     return render(request, 'sales/sale.html', context)