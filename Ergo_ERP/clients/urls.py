from django.urls import path

from Ergo_ERP.clients.views import ClientsList, ClientsCreateView

urlpatterns = [
    path('list/', ClientsList.as_view(), name='clients_list'),
    path('new/', ClientsCreateView.as_view(), name='clients_create'),
]
