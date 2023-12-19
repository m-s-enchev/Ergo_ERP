from django.shortcuts import render
from django.views.generic import FormView

from Ergo_ERP.sales.forms import SalesDocumentForm


# Create your views here.

class SalesDocumentView(FormView):
    template_name = "sales/sale.html"
    form_class = SalesDocumentForm
    success_url = "/"
