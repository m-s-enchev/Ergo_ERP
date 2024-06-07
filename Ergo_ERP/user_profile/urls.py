from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LogoutView
from django.urls import path

from Ergo_ERP.user_profile.views import UserLogin, UserCreate

urlpatterns = [
    path('login/', UserLogin.as_view(), name='user-login'),
    path('logout/', LogoutView.as_view(), name='user-logout'),
    path('create/', login_required(UserCreate.as_view(), login_url='/user/login/'), name='user-create'),
]