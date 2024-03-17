from django.forms import ModelForm

from Ergo_ERP.products.models import ProductsModel


class ProductsModelForm(ModelForm):
    class Meta:
        model = ProductsModel
        fields = "__all__"

