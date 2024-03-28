from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.contrib.auth.views import LoginView, LogoutView
from django.urls import reverse_lazy
from django.views.generic import CreateView


class UserLogin(LoginView):
    template_name = 'user_profile/user-login.html'


class UserCreate(CreateView):
    model = User
    template_name = 'user_profile/user-create.html'
    form_class = UserCreationForm
    success_url = reverse_lazy('homepage')

