from django.forms import forms
from django.shortcuts import render, redirect
from django.urls import reverse

from Ergo_ERP.sales.forms import SalesDocumentForm, SoldProductsFormSet, InvoiceDataFormSet


def sales_document(request):
    if request.method == 'POST':
        sales_document_form = SalesDocumentForm(request.POST)
        sold_products_formset = SoldProductsFormSet(request.POST, prefix='sold_products')
        invoice_data_formset = InvoiceDataFormSet(request.POST, prefix='invoice_data')

        if sales_document_form.is_valid() and sold_products_formset.is_valid() and sold_products_formset.has_changed():
            sales_document_instance = sales_document_form.save()

            for sold_products_form in sold_products_formset:
                if sold_products_form.cleaned_data:
                    sold_products_instance = sold_products_form.save(commit=False)
                    sold_products_instance.sales_document_in_which_sold = sales_document_instance
                    sold_products_instance.save()
            if invoice_data_formset.is_valid() and invoice_data_formset.has_changed():
                for invoice_data_form in invoice_data_formset:
                    if invoice_data_form.cleaned_data:
                        invoice_data_instance = invoice_data_form.save(commit=False)
                        invoice_data_instance.sales_document_for_invoice = sales_document_instance
                        invoice_data_instance.save()

            return redirect(reverse('sale_new'))

    else:
        sales_document_form = SalesDocumentForm()
        sold_products_formset = SoldProductsFormSet(prefix='sold_products')
        invoice_data_formset = InvoiceDataFormSet(prefix='invoice_data')

    context = {
        'sales_document_form': sales_document_form,
        'sold_products_formset': sold_products_formset,
        'invoice_data_formset': invoice_data_formset,
    }
    return render(request, 'sales/sale.html', context)

#########################################################################
#
# def sales_document(request):
#     if request.method == 'POST':
#         sales_document_form = SalesDocumentForm(request.POST)
#         sold_products_formset = SoldProductsFormSet(request.POST, prefix='sold_products')
#         invoice_data_formset = InvoiceDataFormSet(request.POST, prefix='invoice_data')
#
#         # Check if the formset is completely empty
#         if not all([sold_products_formset, invoice_data_formset]) or \
#                 not all([form.is_valid() for form in sold_products_formset.forms + invoice_data_formset.forms]):
#             # If the formset is completely empty, consider the form invalid
#             sales_document_form.add_error(None, 'At least one product or invoice data is required.')
#         else:
#             if sales_document_form.is_valid():
#                 sales_document_instance = sales_document_form.save()
#
#                 for sold_products_form in sold_products_formset:
#                     if sold_products_form.cleaned_data:
#                         sold_products_instance = sold_products_form.save(commit=False)
#                         sold_products_instance.sales_document_in_which_sold = sales_document_instance
#                         sold_products_instance.save()
#
#                 for invoice_data_form in invoice_data_formset:
#                     if invoice_data_form.cleaned_data:
#                         invoice_data_instance = invoice_data_form.save(commit=False)
#                         invoice_data_instance.sales_document_for_invoice = sales_document_instance
#                         invoice_data_instance.save()
#
#                 return redirect(reverse('sale_new'))
#
#     else:
#         sales_document_form = SalesDocumentForm()
#         sold_products_formset = SoldProductsFormSet(prefix='sold_products', formset=EmptyFormSet)
#         invoice_data_formset = InvoiceDataFormSet(prefix='invoice_data', formset=EmptyFormSet)
#
#     context = {
#         'sales_document_form': sales_document_form,
#         'sold_products_formset': sold_products_formset,
#         'invoice_data_formset': invoice_data_formset,
#     }
#     return render(request, 'sales/sale.html', context)

