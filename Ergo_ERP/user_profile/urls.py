from django.contrib.auth.views import LogoutView
from django.urls import path

from Ergo_ERP.user_profile.views import UserLogin, UserCreate

urlpatterns = [
    path('login/', UserLogin.as_view(), name='user-login'),
    path('logout/', LogoutView.as_view(), name='user-logout'),
    path('create/', UserCreate.as_view(), name='user-create'),
]