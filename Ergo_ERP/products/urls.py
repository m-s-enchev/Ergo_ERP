from django.urls import path

from Ergo_ERP.products.views import ProductsList, ProductsCreate, ProductsEdit, ProductsDelete

urlpatterns = [
    path('', ProductsList.as_view(), name='products_list'),
    path('new/', ProductsCreate.as_view(), name='products_create'),
    path('edit/<int:pk>/', ProductsEdit.as_view(), name='products_edit'),
    path('delete/<int:pk>/', ProductsDelete.as_view(), name='products_delete')
]
