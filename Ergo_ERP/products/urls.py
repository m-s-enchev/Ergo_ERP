from django.urls import path

from Ergo_ERP.products.views import ProductsListView, ProductsCreateView

urlpatterns = [
    path('', ProductsListView.as_view(), name='products_list'),
    path('new/', ProductsCreateView.as_view(), name='products_create'),
]