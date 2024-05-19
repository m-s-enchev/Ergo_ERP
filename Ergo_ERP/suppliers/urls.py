from django.urls import path

from Ergo_ERP.suppliers.views import SuppliersList, SuppliersCreate, SuppliersEdit, SuppliersDelete

urlpatterns = [
    path('list/', SuppliersList.as_view(), name='suppliers_list'),
    path('new/', SuppliersCreate.as_view(), name='suppliers_create'),
    path('edit/<int:pk>', SuppliersEdit.as_view(), name='suppliers_edit'),
    path('delete/<int:pk>', SuppliersDelete.as_view(), name='suppliers_delete')
]