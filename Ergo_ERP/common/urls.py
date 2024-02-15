from django.urls import path

from Ergo_ERP.common.views import get_product_price

urlpatterns = [
    path('get-product-price/', get_product_price, name='get_product_price'),
]