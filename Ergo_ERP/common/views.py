from django.db.models import Q
from django.http import JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse

from Ergo_ERP.clients.models import Clients
from Ergo_ERP.common.helper_functions import inventory_products_dict, products_all_dict, add_document_type
from Ergo_ERP.inventory.models import Inventory, ReceivingDocument, ShippingDocument
from Ergo_ERP.products.models import ProductsModel
from Ergo_ERP.sales.models import SalesDocument
from Ergo_ERP.user_settings.models import UserSettings


def homepage_view(request):
    if request.user.is_authenticated:
        user_settings = get_object_or_404(UserSettings, user=request.user)
        context = {
            'user_settings': user_settings,
            'template_verbose_name': 'Main menu'
        }
        return render(request, 'homepage.html', context=context)
    else:
        return redirect(reverse('user-login'))


def get_product_price(request):
    """
    Returns one of the 3 prices of a product from ProductModel
    """
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


def get_purchase_price(request):
    """
    Returns the purchase price of a product from Inventory model
    """
    product_name = request.GET.get('product_name', None)
    if product_name:
        product = Inventory.objects.filter(product_name=product_name).first()
        if product:
            return JsonResponse({
                'product_purchase_price': getattr(product, 'product_purchase_price', None),
                'product_unit': getattr(product, 'product_unit', None)
            })
        else:
            return JsonResponse({'product_price': None, 'product_vat': None})
    else:
        return JsonResponse({'error': 'Invalid request'}, status=400)


def get_products_by_department(request):
    department_id = request.GET.get('department_id')
    if department_id:
        products_dropdown = inventory_products_dict(department_id)
        return JsonResponse(products_dropdown, safe=False)
    else:
        return JsonResponse({'error': 'Department not provided'}, status=400)


def get_products_all(request):
    products_dropdown = products_all_dict()
    return JsonResponse(products_dropdown, safe=False)


def get_client_names(request):
    """
    Returns a list of all instances in Clients.
    """
    term = request.GET.get('term', '')
    clients = Clients.objects.filter(
        Q(client_names__icontains=term) |
        Q(client_phone_number__icontains=term) |
        Q(client_email__icontains=term) |
        Q(client_identification_number__icontains=term)
    ).values(
        'client_names',
        'client_phone_number',
        'client_email',
        'client_identification_number',
        'client_address',
        'client_accountable_person'
    )
    clients_list = list(clients)
    for client in clients_list:
        for key, value in client.items():
            if value is None:
                client[key] = ""
    return JsonResponse(clients_list, safe=False)


def documents_list_view(request):
    sales_documents = SalesDocument.objects.all()
    receive_documents = ReceivingDocument.objects.all()
    shipping_documents = ShippingDocument.objects.all()
    combined_list = sorted(
        list(sales_documents)+list(receive_documents)+list(shipping_documents),
        key=lambda x: (x.date, x.time)
    )
    final_list = add_document_type(combined_list)
    context = {
        'final_list': final_list,
        'template_verbose_name': 'Documents',
    }
    return render(request, template_name='documents-list.html', context=context)





