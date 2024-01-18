from django.urls import path

from Ergo_ERP.sales.views import sales_document_create

urlpatterns = [
    path('new/', sales_document_create, name='sale_new'),
]