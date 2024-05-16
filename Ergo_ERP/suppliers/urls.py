from django.urls import path

from Ergo_ERP.suppliers.views import SuppliersList

urlpatterns = [
    path('list/', SuppliersList.as_view(), name='suppliers-list')
]