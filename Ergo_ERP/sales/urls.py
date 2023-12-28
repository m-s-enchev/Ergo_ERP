from django.urls import path

from Ergo_ERP.sales.views import SalesDocumentView, sales_document

urlpatterns = [
    path('new/', sales_document, name='sale_new'),
]