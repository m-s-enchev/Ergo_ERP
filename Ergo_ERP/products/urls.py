from django.urls import path

from Ergo_ERP.products.views import ProductsListView, ProductsCreateView, ProductsEditView, ProductsDeleteView

urlpatterns = [
    path('', ProductsListView.as_view(), name='products_list'),
    path('new/', ProductsCreateView.as_view(), name='products_create'),
    path('edit/<int:pk>/', ProductsEditView.as_view(), name='products_edit'),
    path('delete/<int:pk>/', ProductsDeleteView.as_view(), name='products_delete')
]
