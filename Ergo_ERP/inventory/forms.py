from django import forms
from datetime import date
from django.forms import inlineformset_factory
from Ergo_ERP.inventory.models import Department, ReceivingDocument, ReceivedProducts, \
    ShippedProducts, ShippingDocument


class DepartmentForm(forms.ModelForm):
    class Meta:
        model = Department
        fields = '__all__'


class TransferDocumentForm(forms.ModelForm):
    date = forms.DateField(
        initial=date.today(),
        input_formats=['%d.%m.%Y'],
        widget=forms.DateInput(format='%d.%m.%Y', attrs={'class': 'datepicker'})
    )
    total_sum = forms.DecimalField(widget=forms.NumberInput(attrs={'readonly': True}))


class ReceivingDocumentForm(TransferDocumentForm):
    class Meta:
        model = ReceivingDocument
        fields = '__all__'


class ShippingDocumentForm(forms.ModelForm):
    class Meta:
        model = ShippingDocument
        fields = '__all__'


class TransferredProductsForm(forms.ModelForm):
    product_exp_date = forms.DateField(
        required=False,
        input_formats=['%d.%m.%Y'],
        widget=forms.DateInput(format='%d.%m.%Y', attrs={'class': 'datepicker'})
    )


class ReceivedProductsForm(TransferredProductsForm):
    class Meta:
        model = ReceivedProducts
        fields = '__all__'


ReceivedProductsFormSet = inlineformset_factory(
    ReceivingDocument,
    ReceivedProducts,
    form=ReceivedProductsForm,
    extra=1,
    can_delete=False,
)


class ShippedProductsForm(TransferredProductsForm):
    class Meta:
        model = ShippedProducts
        fields = '__all__'


ShippedProductsFormSet = inlineformset_factory(
    ShippingDocument,
    ShippedProducts,
    form=ShippedProductsForm,
    extra=1,
    can_delete=False,
)
