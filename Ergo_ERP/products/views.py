from django.shortcuts import render
from django.views.generic import ListView

from Ergo_ERP.products.models import ProductsModel


# Create your views here.

class ProductsListView(ListView):
    model = ProductsModel
    template_name = 'products/products-list.html'
    context_object_name = 'products_list'


