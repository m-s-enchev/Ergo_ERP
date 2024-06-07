from django.contrib.auth.decorators import login_required
from django.urls import path

from Ergo_ERP.sales.views import sales_document_create_view

urlpatterns = [
    path('new/', login_required(sales_document_create_view, login_url='/user/login'), name='sale_new'),
]