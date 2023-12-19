from django.urls import path

from Ergo_ERP.sales.views import SalesDocumentView

urlpatterns = [
    path('new/', SalesDocumentView.as_view(), name='sale_new'),
]