from django.core.exceptions import ValidationError

from Ergo_ERP.inventory.models import Inventory


def check_inventory(document_form, products_formset):
    """
    A custom validation in shipping/sales operations.
    Check if the product and lot exist in the specified Department in Inventory.
    If not adds form error. Then check if there is sufficient quantity, if not
    adds form error.
    """
    all_valid = True
    department = document_form.cleaned_data.get('department') \
                 or document_form.cleaned_data.get('shipping_department')
    for form in products_formset:
        cleaned_data = form.cleaned_data
        product_name = cleaned_data.get('product_name')
        product_lot_number = cleaned_data.get('product_lot_number')
        product_quantity = cleaned_data.get('product_quantity')
        matching_inventory = Inventory.objects.filter(
            product_name=product_name,
            product_lot_number=product_lot_number,
            department=department
        )
        if matching_inventory.exists():
            matching_instance = matching_inventory.first()
            if matching_instance.product_quantity < product_quantity:
                form.add_error('product_quantity', "Insufficient quantity !")
                all_valid = False
        else:
            form.add_error('product_name', "No such product or lot !")
            all_valid = False
        return all_valid


def create_inventory_instance(product_instance):
    """
    Creates a new instance of a product and lot in Inventory
    """
    new_inventory_instance = Inventory()
    field_names = [field.name for field in new_inventory_instance._meta.fields if field.name != 'id']
    for field_name in field_names:
        setattr(new_inventory_instance, field_name, getattr(product_instance, field_name))
    new_inventory_instance.save()


def receive_in_inventory(matching_inventory_instance, product_instance):
    """
    Updates product quantities, value and median price, when receiving goods in inventory
    """
    if matching_inventory_instance:
        matching_inventory_instance.product_quantity += product_instance.product_quantity
        matching_inventory_instance.product_total += product_instance.product_total
        matching_inventory_instance.purchase_price = (matching_inventory_instance.product_total /
                                                      matching_inventory_instance.product_quantity)
        matching_inventory_instance.save()
    else:
        create_inventory_instance(product_instance)


def subtract_from_inventory(matching_inventory_instance, product_instance):
    """
    Updates product quantities and value, when shipping/selling goods from inventory
    """
    if matching_inventory_instance.product_quantity < product_instance.product_quantity:
        raise ValidationError(f"There is not enough of product {matching_inventory_instance.product_name} "
                              f"with lot {matching_inventory_instance.product_lot_number}.")
    else:
        matching_inventory_instance.product_quantity -= product_instance.product_quantity
        matching_inventory_instance.product_total -= (product_instance.product_quantity *
                                                      matching_inventory_instance.product_purchase_price)
        matching_inventory_instance.save()


def update_inventory(product_instances, is_receiving: bool, department):
    """
    Adds to and removes from quantities and value of existing products.
    Adjusts current median purchase price.
    Creates new product lots in inventory if necessary.
    """
    for product_instance in product_instances:
        matching_inventory_instance = Inventory.objects.filter(
            product_name=product_instance.product_name,
            product_lot_number=product_instance.product_lot_number,
            department=department
        ).first()

        if is_receiving:
            receive_in_inventory(matching_inventory_instance, product_instance)
        else:
            subtract_from_inventory(matching_inventory_instance, product_instance)