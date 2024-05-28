from django.db.models import Q
from django.http import JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse

from Ergo_ERP.clients.models import Clients
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


def inventory_products_dict(department=None):
    """
    Filters Inventory instances by Department and returns a dictionary
    of product names, quantities, units, lots and exp. dates.
    """
    if department is not None:
        products = Inventory.objects.filter(department=department)
    else:
        products = Inventory.objects.all()
    products_dict = {}
    for product in products:
        if product.product_exp_date:
            exp_date_formatted = product.product_exp_date.strftime('%d.%m.%Y')
            lot_number = product.product_lot_number
        else:
            exp_date_formatted = ""
            lot_number = ""
        products_dict[product.product_name] = [
            format(product.product_quantity.normalize(), 'f'),
            product.product_unit,
            lot_number,
            exp_date_formatted
            ]
    return products_dict


def get_products_by_department(request):
    department_id = request.GET.get('department_id')
    if department_id:
        products_dropdown = inventory_products_dict(department_id)
        return JsonResponse(products_dropdown, safe=False)
    else:
        return JsonResponse({'error': 'Department not provided'}, status=400)


def products_all_dict():
    """
    Returns a dictionary of all instances in ProductsModel, with
    product names, quantities, units, lots and exp. dates.
    """
    products = ProductsModel.objects.all()
    products_dict = {}
    for product in products:
        products_dict[product.product_name] = product.product_unit
    return products_dict


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
    sales_documents = list(SalesDocument.objects.all())
    receive_documents = list(ReceivingDocument.objects.all())
    shipping_documents = list(ShippingDocument.objects.all())

    final_list = sales_documents+receive_documents+shipping_documents
    print(final_list)
    context = {
        'final_list': final_list,
        'template_verbose_name': 'Documents'
    }
    return render(request, template_name='documents-list.html', context=context)





