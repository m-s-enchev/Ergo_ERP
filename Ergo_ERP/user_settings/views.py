from django.shortcuts import render, redirect
from django.urls import reverse

from Ergo_ERP.user_settings.forms import UserSettingsForm
from Ergo_ERP.user_settings.models import UserSettings


def user_settings_view(request):
    if request.method == 'POST':
        user_settings_form = UserSettingsForm(request.POST)
        if user_settings_form.is_valid():
            user_settings_form.save()
            return redirect(reverse('settings'))
    else:
        user_instance = UserSettings.objects.get(user=request.user)
        user_settings_form = UserSettingsForm(instance=user_instance)

    context = {
        'user_settings_form': user_settings_form,
        'template_verbose_name': 'Settings'
    }

    return render(request, 'settings.html', context)

