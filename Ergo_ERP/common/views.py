from django.http import JsonResponse

from Ergo_ERP.inventory.models import Inventory
from Ergo_ERP.products.models import ProductsModel


# def get_product_price(request):
#     product_name = request.GET.get('product_name', None)
#     model_name = request.GET.get('model_name', None)
#     product_lot = request.GET.get('product_lot', None)  # Optional parameter for product_lot
#
#     if product_name and model_name:
#         if model_name == 'product':
#             model = ProductsModel
#             price_field_name = 'product_retail_price'
#             product = model.objects.filter(product_name=product_name).first()
#         elif model_name == 'inventory':
#             model = Inventory
#             price_field_name = 'product_purchase_price'
#             product = model.objects.filter(product_name=product_name, product_lot=product_lot).first()
#         else:
#             return JsonResponse({'error': 'Invalid model name in request'}, status=400)
#
#         if product:
#             return JsonResponse({
#                 'product_price': getattr(product, price_field_name, None),
#                 'product_vat': getattr(product, 'product_vat', None)
#             })
#         else:
#             return JsonResponse({'product_price': None, 'product_vat': None})
#     else:
#         return JsonResponse({'error': 'Invalid request'}, status=400)


def get_product_price(request):
    product_name = request.GET.get('product_name', None)
    price_type = request.GET.get('price_type', None)
    if product_name:
        product = ProductsModel.objects.filter(product_name=product_name).first()

        if product:
            return JsonResponse({
                'product_price': getattr(product, price_type, None),
                'product_vat': getattr(product, 'product_vat', None)
            })
        else:
            return JsonResponse({'product_price': None, 'product_vat': None})
    else:
        return JsonResponse({'error': 'Invalid request'}, status=400)
