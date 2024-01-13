from django import forms
from django.forms import inlineformset_factory, BaseInlineFormSet, ModelForm

from Ergo_ERP.sales.models import SalesDocument, SoldProducts, InvoiceData

from datetime import date


class InvoiceDataForm(forms.ModelForm):
    invoice_date = forms.DateField(initial=date.today())
    invoice_due_date = forms.DateField(initial=date.today())

    class Meta:
        model = InvoiceData
        fields = '__all__'


class SalesDocumentForm(ModelForm):
    date = forms.DateField(initial=date.today(), required=False)

    class Meta:
        model = SalesDocument
        fields = '__all__'


class SoldProductsForm(ModelForm):
    class Meta:
        model = SoldProducts
        fields = '__all__'


class InlineFormSetWithNoEmptyForms(BaseInlineFormSet):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for form in self.forms:
            form.empty_permitted = False


SoldProductsFormSet = inlineformset_factory(
    SalesDocument,
    SoldProducts,
    form=SoldProductsForm,
    extra=1,
    can_delete=False,
    formset=InlineFormSetWithNoEmptyForms
)

InvoiceDataFormSet = inlineformset_factory(
    SalesDocument,
    InvoiceData,
    form=InvoiceDataForm,
    extra=1,
    can_delete=False,
    formset=InlineFormSetWithNoEmptyForms
)
