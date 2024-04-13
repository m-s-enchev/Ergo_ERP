from django.urls import path

from Ergo_ERP.common.views import get_product_price, get_products_by_department, get_client_names, homepage_view, \
    get_products_all, get_purchase_price

urlpatterns = [
    path('', homepage_view, name='homepage'),
    path('get-product-price/', get_product_price, name='get_product_price'),
    path('get-purchase-price/', get_purchase_price, name='get_purchase_price'),
    path('get-products-by-department/', get_products_by_department, name='get-products-by-department'),
    path('get-products-all/', get_products_all, name='get-products-all'),
    path('get-client-names/', get_client_names, name='get-client-names'),
]