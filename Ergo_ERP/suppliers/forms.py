from django.forms import ModelForm

from Ergo_ERP.suppliers.models import Suppliers


class SuppliersModelForm (ModelForm):
    class Meta:
        model = Suppliers
        fields = "__all__"
