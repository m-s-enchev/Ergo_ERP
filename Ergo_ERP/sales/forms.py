from django import forms
from django.forms import inlineformset_factory, BaseInlineFormSet, ModelForm

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
        fields = '__all__'


class SoldProductsForm(ModelForm):
    class Meta:
        model = SoldProducts
        fields = '__all__'


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


