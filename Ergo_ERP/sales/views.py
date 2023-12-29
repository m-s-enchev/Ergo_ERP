from django.shortcuts import render, redirect
from django.urls import reverse
from django.views.generic import FormView

from Ergo_ERP.sales.forms import SalesDocumentForm, SoldProductsFormSet


# Create your views here.

# class SalesDocumentView(FormView):
#     template_name = "sales/sale.html"
#     form_class = SalesDocumentForm
#     success_url = "/"


def sales_document(request):
    if request.method == 'POST':
        sales_document_form = SalesDocumentForm(request.POST)
        sold_products_formset = SoldProductsFormSet(request.POST, prefix='sold_products')

        if sales_document_form.is_valid() and sold_products_formset.is_valid():
            sales_document = sales_document_form.save()

            for form in sold_products_formset:
                if form.cleaned_data:
                    sold_product = form.save(commit=False)
                    sold_product.sales_document_in_which_sold = sales_document
                    sold_product.save()

            return redirect(reverse('sale_new'))

    else:
        sales_document_form = SalesDocumentForm()
        sold_products_formset = SoldProductsFormSet(prefix='sold_products')
    context = {
        'sales_document_form': sales_document_form,
        'sold_products_formset': sold_products_formset
    }

    return render(request, 'sales/sale.html', context)
