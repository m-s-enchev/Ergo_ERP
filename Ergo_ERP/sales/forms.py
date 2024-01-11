from django.forms import ModelForm, inlineformset_factory, forms, BaseInlineFormSet

from Ergo_ERP.sales.models import SalesDocument, SoldProducts, InvoiceData


class InvoiceDataForm(ModelForm):
    class Meta:
        model = InvoiceData
        fields = '__all__'


class SalesDocumentForm(ModelForm):

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
