from django.urls import path

from Ergo_ERP.clients.views import ClientsList, ClientsCreate, ClientsEdit, ClientsDelete

urlpatterns = [
    path('list/', ClientsList.as_view(), name='clients_list'),
    path('new/', ClientsCreate.as_view(), name='clients_create'),
    path('edit/<int:pk>/', ClientsEdit.as_view(), name='clients_edit'),
    path('delete/<int:pk>/', ClientsDelete.as_view(), name='clients_delete'),
]
