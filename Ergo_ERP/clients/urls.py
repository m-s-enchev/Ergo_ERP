from django.contrib.auth.decorators import login_required
from django.urls import path

from Ergo_ERP.clients.views import ClientsList, ClientsCreate, ClientsEdit, ClientsDelete

urlpatterns = [
    path('list/', login_required(ClientsList.as_view(), login_url='/user/login'), name='clients_list'),
    path('new/', login_required(ClientsCreate.as_view(), login_url='/user/login'), name='clients_create'),
    path('edit/<int:pk>/', login_required(ClientsEdit.as_view(), login_url='/user/login'), name='clients_edit'),
    path('delete/<int:pk>/', login_required(ClientsDelete.as_view(), login_url='/user/login'), name='clients_delete'),
]
