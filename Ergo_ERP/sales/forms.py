from django import forms

from django.forms import inlineformset_factory,  ModelForm

from Ergo_ERP.common.forms import DecimalFieldsValidationMixin
from Ergo_ERP.sales.models import SalesDocument, SoldProducts, InvoiceData, InvoicedProducts
from datetime import date


class InvoiceDataForm(forms.ModelForm):
    invoice_date = forms.DateField(
        initial=date.today(),
        input_formats=['%d.%m.%Y'],
        widget=forms.DateInput(format='%d.%m.%Y', attrs={'class': 'datepicker'})
    )
    invoice_due_date = forms.DateField(
        initial=date.today(),
        input_formats=['%d.%m.%Y'],
        widget=forms.DateInput(format='%d.%m.%Y', attrs={'class': 'datepicker'})
    )

    class Meta:
        model = InvoiceData
        fields = '__all__'
        exclude = ['sales_document_for_invoice']


class SalesDocumentForm(ModelForm):
    date = forms.DateField(
        initial=date.today(),
        input_formats=['%d.%m.%Y'],
        widget=forms.DateInput(format='%d.%m.%Y', attrs={'class': 'datepicker'})
    )
    sale_total_before_tax = forms.DecimalField(widget=forms.NumberInput(attrs={'readonly': True}))
    sale_total_tax = forms.DecimalField(widget=forms.NumberInput(attrs={'readonly': True}))
    sale_total_final = forms.DecimalField(widget=forms.NumberInput(attrs={'readonly': True}))

    class Meta:
        model = SalesDocument
        exclude = ('operator',)


class SoldProductsForm(ModelForm, DecimalFieldsValidationMixin):
    product_unit = forms.CharField(widget=forms.TextInput(attrs={'readonly': True}))
    product_exp_date = forms.DateField(input_formats=['%d.%m.%Y'], required=False,
                                       widget=forms.DateInput(attrs={'readonly': True}))
    product_lot_number = forms.CharField(required=False, widget=forms.TextInput(attrs={'readonly': True}))
    product_total_before_tax = forms.CharField(widget=forms.NumberInput(attrs={'readonly': True}))
    product_total = forms.CharField(widget=forms.NumberInput(attrs={'readonly': True}))

    class Meta:
        model = SoldProducts
        fields = '__all__'

    def clean_product_exp_date(self):
        data = self.cleaned_data['product_exp_date']
        return data

    def __init__(self, *args, **kwargs):
        super(SoldProductsForm, self).__init__(*args, **kwargs)
        for field in self.fields.values():
            field.error_messages = {'required': 'Required'}


class InvoicedProductsForm(ModelForm):
    class Meta:
        model = InvoicedProducts
        fields = '__all__'


SoldProductsFormSet = inlineformset_factory(
    SalesDocument,
    SoldProducts,
    form=SoldProductsForm,
    extra=1,
    can_delete=False,
)


