from django.db import DatabaseError
from django.db.models import Max

from Ergo_ERP.inventory.models import Inventory
from Ergo_ERP.products.models import ProductsModel


def is_formset_nonempty(formset):
    """
    Checks if there is at least one nonempty form in the formset.
    """
    for form in formset:
        if form.cleaned_data:
            return True
    return False


def products_list_save_to_document(products_formset, document_instance, name_of_foreignkey_field: str, department=None):
    """
    Handles product forms in a formset and links their instances to the document instance.
    Returns a list of saved instances.
    """
    saved_product_instances = []
    for products_form in products_formset:
        if products_form.cleaned_data:
            products_instance = products_form.save(commit=False)
            setattr(products_instance, name_of_foreignkey_field, document_instance)
            if department:
                setattr(products_instance, 'department', department)
            try:
                products_instance.save()
            except DatabaseError as de:
                raise DatabaseError(f"Database error while saving Product instance: {de}")
            except Exception as e:
                raise Exception(f"An unexpected error occurred while saving Product instance: {e}")
            saved_product_instances.append(products_instance)
    return saved_product_instances


def get_next_document_number(model, numerator_field_name):
    """
    Checks what is the last numerator field value in a model and determines the next one.
    Used for invoice document numbers which are separate from their Ids
    """
    last_number = model.objects.aggregate(Max(numerator_field_name))[f'{numerator_field_name}__max']
    if last_number is None:
        document_number = 1
    else:
        document_number = last_number + 1
    return document_number


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


def check_product_name(products_formset):
    """
    Check if a product name is present in ProductsModel and is therefore a valid entry in the form
    """
    valid_name = True
    for form in products_formset:
        cleaned_data = form.cleaned_data
        product_name = cleaned_data.get('product_name')
        matching_product = ProductsModel.objects.filter(product_name=product_name)
        if product_name and not matching_product.exists():
            form.add_error('product_name', "No such product!")
            valid_name = False
    return valid_name


def two_column_products_dict():
    """
    Returns a simple list of product names specifically for Warehouse Receiving
    """
    products = ProductsModel.objects.all()
    products_names = []
    for product in products:
        products_names.append(product.product_name)
    return products_names

