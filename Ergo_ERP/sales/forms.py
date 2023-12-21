from django.forms import ModelForm, TextInput

from Ergo_ERP.sales.models import SalesDocument


class SalesDocumentForm(ModelForm):

    class Meta:
        model = SalesDocument
        fields = '__all__'


