from django.urls import path

from Ergo_ERP.clients.views import ClientsList

urlpatterns = [
    path('list/', ClientsList.as_view(), name='clients-list'),
]