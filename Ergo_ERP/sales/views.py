from django.shortcuts import render, redirect
from django.urls import reverse

from Ergo_ERP.sales.forms import SalesDocumentForm, SoldProductsFormSet, InvoiceDataFormSet


def sales_document(request):
    if request.method == 'POST':
        sales_document_form = SalesDocumentForm(request.POST)
        sold_products_formset = SoldProductsFormSet(request.POST, prefix='sold_products')
        invoice_data_formset = InvoiceDataFormSet(request.POST, prefix='invoice_data')
        print(invoice_data_formset)

        if (
                sales_document_form.is_valid()
                and sold_products_formset.is_valid()
                and (not invoice_data_formset.forms or invoice_data_formset.is_valid())
        ):
            print('forms are valid bro')
            sales_document = sales_document_form.save()
            sold_products_instances = sold_products_formset.save(commit=False)

            for sold_product, form in zip(sold_products_instances, sold_products_formset):
                if form.cleaned_data:
                    sold_product.sales_document_in_which_sold = sales_document
                    sold_product.save()
            if invoice_data_formset.forms:
                invoice_data_instances = invoice_data_formset.save(commit=False)
                for invoice_data_instance, form in zip(invoice_data_instances, invoice_data_formset):
                    if form.cleaned_data:
                        invoice_data_instance.sales_document = sales_document
                        invoice_data_instance.save()

                sold_products_formset.save_m2m()
                invoice_data_formset.save_m2m()

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

    # if request.method == 'POST':
    #     sales_document_form = SalesDocumentForm(request.POST)
    #     sold_products_formset = SoldProductsFormSet(request.POST, prefix='sold_products')
    #
    #     if sales_document_form.is_valid() and sold_products_formset.is_valid():
    #         sales_document = sales_document_form.save()
    #
    #         for form in sold_products_formset:
    #             if form.cleaned_data:
    #                 sold_product = form.save(commit=False)
    #                 sold_product.sales_document_in_which_sold = sales_document
    #                 sold_product.save()
    #
    #         return redirect(reverse('sale_new'))
    #
    # else:
    #     sales_document_form = SalesDocumentForm()
    #     sold_products_formset = SoldProductsFormSet(prefix='sold_products')
    #
    # context = {
    #     'sales_document_form': sales_document_form,
    #     'sold_products_formset': sold_products_formset,
    # }
    # return render(request, 'sales/sale.html', context)
