"""
URL configuration for Ergo_ERP project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.views.generic import TemplateView

from Ergo_ERP.user_settings.views import user_settings_view

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('Ergo_ERP.common.urls')),
    path('settings/', user_settings_view, name='settings'),
    path('clients/', include('Ergo_ERP.clients.urls')),
    path('suppliers/', include('Ergo_ERP.suppliers.urls')),
    path('sales/', include('Ergo_ERP.sales.urls')),
    path('inventory/', include('Ergo_ERP.inventory.urls')),
    path('products/', include('Ergo_ERP.products.urls')),
    path('common/', include('Ergo_ERP.common.urls')),
    path('user/', include('Ergo_ERP.user_profile.urls')),
]
