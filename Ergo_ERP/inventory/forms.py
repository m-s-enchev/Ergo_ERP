from django import forms
from datetime import date
from django.forms import inlineformset_factory
from Ergo_ERP.inventory.models import WarehouseDocument, TransferredProducts, Department


class DepartmentForm(forms.ModelForm):
    class Meta:
        model = Department
        fields = '__all__'


class WarehouseDocumentForm(forms.ModelForm):
    date = forms.DateField(
        initial=date.today(),
        input_formats=['%d.%m.%Y'],
        widget=forms.DateInput(format='%d.%m.%Y', attrs={'class': 'datepicker'})
    )

    class Meta:
        model = WarehouseDocument
        fields = '__all__'


class TransferredProductsForm(forms.ModelForm):
    product_exp_date = forms.DateField(
        required=False,
        input_formats=['%d.%m.%Y'],
        widget=forms.DateInput(format='%d.%m.%Y', attrs={'class': 'datepicker'})
    )

    class Meta:
        model = TransferredProducts
        fields = '__all__'


TransferredProductsFormSet = inlineformset_factory(
    WarehouseDocument,
    TransferredProducts,
    form=TransferredProductsForm,
    extra=1,
    can_delete=False,
)
