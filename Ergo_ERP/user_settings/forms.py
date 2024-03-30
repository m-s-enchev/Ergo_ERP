from django.forms import ModelForm

from Ergo_ERP.user_settings.models import UserSettings


class UserSettingsForm(ModelForm):
    class Meta:
        model = UserSettings
        exclude = ('user',)

