from django.urls import path

from Ergo_ERP.inventory.views import InventoryView, receiving_document_create

urlpatterns = [
    path('', InventoryView.as_view(), name='inventory'),
    path('receive/', receiving_document_create, name='receive-goods'),
]
