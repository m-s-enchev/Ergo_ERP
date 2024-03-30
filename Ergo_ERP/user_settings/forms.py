from django import forms

from Ergo_ERP.user_settings.models import UserSettings


class UserSettingsForm(forms.ModelForm):
    show_main_menu_shortcuts = forms.BooleanField(widget=forms.CheckboxInput, required=False)
    show_sale_quick_select = forms.BooleanField(widget=forms.CheckboxInput, required=False)
    default_sales_doc_is_invoice = forms.BooleanField(widget=forms.CheckboxInput, required=False)
    show_lot_and_exp_columns = forms.BooleanField(widget=forms.CheckboxInput, required=False)

    class Meta:
        model = UserSettings
        exclude = ('user',)

