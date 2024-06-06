from django.urls import path

from Ergo_ERP.inventory.views import InventoryView, receiving_document_create_view, shipping_document_create_view

urlpatterns = [
    path('', InventoryView.as_view(), name='inventory'),
    path('receive/', receiving_document_create_view, name='receive-goods'),
    path('ship/', shipping_document_create_view, name='ship-goods')
]
