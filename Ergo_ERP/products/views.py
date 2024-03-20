from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView

from Ergo_ERP.products.forms import ProductsModelForm
from Ergo_ERP.products.models import ProductsModel


class ProductsListView(ListView):
    model = ProductsModel
    template_name = 'products/products-list.html'
    context_object_name = 'products_list'
    extra_context = {'template_verbose_name': 'Products'}


class ProductsCreateView(CreateView):
    model = ProductsModel
    form_class = ProductsModelForm
    template_name = 'products/products-create.html'
    extra_context = {'template_verbose_name': 'Create product'}

    def get_success_url(self):
        return reverse_lazy('products_create')

