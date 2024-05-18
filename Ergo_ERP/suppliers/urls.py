from django.urls import path

from Ergo_ERP.suppliers.views import SuppliersList, SuppliersCreate

urlpatterns = [
    path('list/', SuppliersList.as_view(), name='suppliers_list'),
    path('new/', SuppliersCreate.as_view(), name='suppliers_create')
]