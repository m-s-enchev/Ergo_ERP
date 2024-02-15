from django.http import JsonResponse
from django.shortcuts import render

from Ergo_ERP.products.models import ProductsModel


def get_product_price(request):
    product_name = request.GET.get('product_name', None)
    if product_name:
        product = ProductsModel.objects.filter(product_name=product_name).first()
        if product:
            return JsonResponse({'product_price': product.product_retail_price})
        else:
            return JsonResponse({'product_price': None})
    return JsonResponse({'error': 'Invalid request'}, status=400)
