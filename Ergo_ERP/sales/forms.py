from django.forms import ModelForm, inlineformset_factory

from Ergo_ERP.sales.models import SalesDocument, SoldProducts


class SalesDocumentForm(ModelForm):

    class Meta:
        model = SalesDocument
        fields = '__all__'


class SoldProductsForm(ModelForm):
    class Meta:
        model = SoldProducts
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.label_suffix = ''


SoldProductsFormSet = inlineformset_factory(
    SalesDocument,
    SoldProducts,
    form=SoldProductsForm,
    extra=1,
    can_delete=False
)
