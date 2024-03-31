from django.http import JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse

from Ergo_ERP.clients.models import Clients
from Ergo_ERP.inventory.models import Inventory
from Ergo_ERP.products.models import ProductsModel
from Ergo_ERP.sales.views import products_dict_dropdown
from Ergo_ERP.user_settings.models import UserSettings


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


def homepage_view(request):

    user_settings = get_object_or_404(UserSettings, user=request.user)
    context = {
        'user_settings': user_settings,
        'template_verbose_name': 'Main menu'
    }
    if request.user.is_authenticated:
        return render(request, 'homepage.html', context=context)
    else:
        return redirect(reverse('user-login'))


def get_product_price(request):
    product_name = request.GET.get('product_name', None)
    price_type = request.GET.get('price_type', None)
    if product_name:
        product = ProductsModel.objects.filter(product_name=product_name).first()

        if product:
            return JsonResponse({
                'product_price': getattr(product, price_type, None),
                'product_vat': getattr(product, 'product_vat', None),
                'product_unit': getattr(product, 'product_unit', None)
            })
        else:
            return JsonResponse({'product_price': None, 'product_vat': None})
    else:
        return JsonResponse({'error': 'Invalid request'}, status=400)


def products_dropdown_update(request):
    department_id = request.GET.get('department_id')
    if department_id:
        products_dropdown = products_dict_dropdown(department_id)
        return JsonResponse(products_dropdown, safe=False)
    else:
        return JsonResponse({'error': 'Department not provided'}, status=400)


def get_client_names(request):
    term = request.GET.get('term')  # jQuery UI sends the term as 'term'
    client_names = Clients.objects.filter(client_names__icontains=term).values_list('client_names', flat=True)
    client_names_list = list(client_names)
    return JsonResponse(client_names_list, safe=False)


