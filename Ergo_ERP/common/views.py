from django.http import JsonResponse

from Ergo_ERP.inventory.models import Inventory
from Ergo_ERP.products.models import ProductsModel


def get_product_price(request):
    product_name = request.GET.get('product_name', None)
    model_type = request.GET.get('model_type', None)

    if product_name and model_type:
        if model_type == 'product':
            model = ProductsModel
            price_field_name = 'product_retail_price'
        elif model_type == 'inventory':
            model = Inventory
            price_field_name = 'product_purchase_price'
        else:
            return JsonResponse({'error': 'Invalid model name in request'}, status=400)

        product = model.objects.filter(product_name=product_name).first()
        if product:
            return JsonResponse({'product_price': getattr(product, price_field_name, None)})
        else:
            return JsonResponse({'product_price': None})
    else:
        return JsonResponse({'error': 'Invalid request'}, status=400)