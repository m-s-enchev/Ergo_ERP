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
    Handles products form and links their instances to the document instance.
    """
    saved_product_instances = []
    for products_form in products_formset:
        if products_form.cleaned_data:
            products_instance = products_form.save(commit=False)
            setattr(products_instance, name_of_foreignkey_field, document_instance)
            if department:
                setattr(products_instance, 'department', department)
            products_instance.save()
            saved_product_instances.append(products_instance)
    return saved_product_instances


def get_next_document_number(model, numerator_field_name):
    """
    Check what is the last numerator field value in a model and determines the next one.
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


def add_document_type(queryset_objects: list, verbose_names_dict:dict):
    """
    Adds a verbose name of the model to it instances in a list
    """
    for obj in queryset_objects:
        obj.document_type = verbose_names_dict[obj._meta.model_name]
    return queryset_objects


def combine_objects_in_list(*args):
    """
    Combines instances of models in one list
    """
    combined_list = []
    for model in args:
        objects_list = model.objects.all()
        combined_list += list(objects_list)
    return combined_list
