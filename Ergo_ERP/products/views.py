from django.shortcuts import render
from django.views.generic import ListView

from Ergo_ERP.products.models import ProductsModel


class ProductsListView(ListView):
    model = ProductsModel
    template_name = 'products/products-list.html'
    context_object_name = 'products_list'
    extra_context = {'template_verbose_name': 'Products'}


