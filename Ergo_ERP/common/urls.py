from django.contrib.auth.decorators import login_required
from django.urls import path
from django.views.generic import TemplateView

from Ergo_ERP.common.views import get_product_price_view, get_products_by_department_view, get_client_names_view, homepage_view, \
    get_products_all_view, get_purchase_price_view, documents_list_view

urlpatterns = [
    path('', login_required(homepage_view, login_url='/user/login'), name='homepage'),
    path('get-product-price/', login_required(get_product_price_view, login_url='/user/login'), name='get_product_price'),
    path('get-purchase-price/',
         login_required(get_purchase_price_view, login_url='/user/login'),
         name='get_purchase_price'),
    path('get-products-by-department/',
         login_required(get_products_by_department_view, login_url='/user/login'),
         name='get-products-by-department'),
    path('get-products-all/', login_required(get_products_all_view, login_url='/user/login'), name='get-products-all'),
    path('get-client-names/', login_required(get_client_names_view, login_url='/user/login'), name='get-client-names'),
    path('documents-list/', login_required(documents_list_view, login_url='/user/login'), name='documents_list'),
    path('401/', TemplateView.as_view(template_name='401.html'), name='401'),
    path('403/', TemplateView.as_view(template_name='403.html'), name='403'),
    path('404/', TemplateView.as_view(template_name='404.html'), name='404'),
    path('500/', TemplateView.as_view(template_name='500.html'), name='500'),
    path('502/', TemplateView.as_view(template_name='502.html'), name='502'),
    path('503/', TemplateView.as_view(template_name='503.html'), name='503'),
    path('504/', TemplateView.as_view(template_name='504.html'), name='504'),
]