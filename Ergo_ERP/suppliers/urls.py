from django.contrib.auth.decorators import login_required
from django.urls import path

from Ergo_ERP.suppliers.views import SuppliersList, SuppliersCreate, SuppliersEdit, SuppliersDelete

urlpatterns = [
    path('list/', login_required(SuppliersList.as_view(), login_url='/user/login'), name='suppliers_list'),
    path('new/', login_required(SuppliersCreate.as_view(), login_url='/user/login'), name='suppliers_create'),
    path('edit/<int:pk>', login_required(SuppliersEdit.as_view(), login_url='/user/login'), name='suppliers_edit'),
    path('delete/<int:pk>', login_required(SuppliersDelete.as_view(), login_url='/user/login'), name='suppliers_delete')
]