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

    class Meta:
        model = SalesDocument
        exclude = ('operator',)


class SoldProductsForm(ModelForm, DecimalFieldsValidationMixin):
    product_exp_date = forms.DateField(
        input_formats=['%d.%m.%Y']
    )

    class Meta:
        model = SoldProducts
        fields = '__all__'

    def clean_product_exp_date(self):
        data = self.cleaned_data['product_exp_date']
        return data


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


