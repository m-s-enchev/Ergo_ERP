from django.urls import path

from Ergo_ERP.sales.views import sales_document_create_view

urlpatterns = [
    path('new/', sales_document_create_view, name='sale_new'),
]