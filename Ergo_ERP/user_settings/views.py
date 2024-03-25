from django.shortcuts import render, redirect
from django.urls import reverse

from Ergo_ERP.user_settings.forms import UserSettingsForm


def user_settings_view(request):

    user_settings_form = UserSettingsForm(request.POST or None)

    if request == 'POST':
        if user_settings_form.is_valid():
            user_settings_form.save()
            return redirect(reverse('settings'))



    context = {
        'user_settings_form': user_settings_form,
        'template_verbose_name': 'Settings'
    }

    return render(request, 'settings.html', context)

