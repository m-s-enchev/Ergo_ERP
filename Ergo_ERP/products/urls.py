from django.contrib.auth.decorators import login_required
from django.urls import path

from Ergo_ERP.products.views import ProductsList, ProductsCreate, ProductsEdit, ProductsDelete

urlpatterns = [
    path('', login_required(ProductsList.as_view(), login_url='/user/login'), name='products_list'),
    path('new/', login_required(ProductsCreate.as_view(), login_url='/user/login'), name='products_create'),
    path('edit/<int:pk>/', login_required(ProductsEdit.as_view(), login_url='/user/login'), name='products_edit'),
    path('delete/<int:pk>/', login_required(ProductsDelete.as_view(), login_url='/user/login'), name='products_delete')
]
