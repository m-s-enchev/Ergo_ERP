from django.urls import path

from Ergo_ERP.common.views import get_product_price, products_dropdown_update

urlpatterns = [
    path('get-product-price/', get_product_price, name='get_product_price'),
    path('products-dropdown-update/', products_dropdown_update, name='products_dropdown_update'),
]