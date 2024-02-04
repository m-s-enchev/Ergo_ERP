from django.urls import path

from Ergo_ERP.products.views import ProductsListView

urlpatterns = [
    path('', ProductsListView.as_view(), name='products_list'),
]