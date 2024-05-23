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
        exclude = ('operator',)


class ShippingDocumentForm(TransferDocumentForm):
    class Meta:
        model = ShippingDocument
        exclude = ('operator',)


class TransferredProductsForm(forms.ModelForm):
    product_unit = forms.CharField(widget=forms.TextInput(attrs={'readonly': True}))
    product_total = forms.CharField(widget=forms.NumberInput(attrs={'readonly': True}))


class ReceivedProductsForm(TransferredProductsForm):
    product_exp_date = forms.DateField(
        required=False,
        input_formats=['%d.%m.%Y'],
        widget=forms.DateInput(format='%d.%m.%Y', attrs={'class': 'datepicker'})
    )
    product_lot_number = forms.CharField(required=False)

    class Meta:
        model = ReceivedProducts
        exclude = ('department',)


ReceivedProductsFormSet = inlineformset_factory(
    ReceivingDocument,
    ReceivedProducts,
    form=ReceivedProductsForm,
    extra=1,
    can_delete=False,
)


class ShippedProductsForm(TransferredProductsForm):
    product_exp_date = forms.DateField(
        required=False,
        input_formats=['%d.%m.%Y'],
        widget=forms.DateInput(format='%d.%m.%Y', attrs={'readonly': True})
    )
    product_lot_number = forms.CharField(required=False, widget=forms.TextInput(attrs={'readonly': True}))

    class Meta:
        model = ShippedProducts
        exclude = ('department',)


ShippedProductsFormSet = inlineformset_factory(
    ShippingDocument,
    ShippedProducts,
    form=ShippedProductsForm,
    extra=1,
    can_delete=False,
)
