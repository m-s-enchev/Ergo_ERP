from django.forms import ModelForm

from Ergo_ERP.clients.models import Clients


class ClientsModelForm (ModelForm):
    class Meta:
        model = Clients
        fields = "__all__"
