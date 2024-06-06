from django.urls import path

from Ergo_ERP.common.views import get_product_price_view, get_products_by_department_view, get_client_names_view, homepage_view, \
    get_products_all_view, get_purchase_price_view, documents_list_view

urlpatterns = [
    path('', homepage_view, name='homepage'),
    path('get-product-price/', get_product_price_view, name='get_product_price'),
    path('get-purchase-price/', get_purchase_price_view, name='get_purchase_price'),
    path('get-products-by-department/', get_products_by_department_view, name='get-products-by-department'),
    path('get-products-all/', get_products_all_view, name='get-products-all'),
    path('get-client-names/', get_client_names_view, name='get-client-names'),
    path('documents-list/', documents_list_view, name='documents_list')
]