from django.contrib.auth.decorators import login_required
from django.urls import path

from Ergo_ERP.inventory.views import InventoryView, receiving_document_create_view, shipping_document_create_view

urlpatterns = [
    path('', login_required(InventoryView.as_view(), login_url='/user/login'), name='inventory'),
    path('receive/', login_required(receiving_document_create_view, login_url='/user/login'), name='receive-goods'),
    path('ship/', login_required(shipping_document_create_view, login_url='/user/login'), name='ship-goods')
]
