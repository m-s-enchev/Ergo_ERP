from django.db.models import Max


def is_formset_nonempty(formset):
    """
    Checks if there is at least one nonempty form in the formset.
    """
    for form in formset:
        if form.cleaned_data:
            return True
    return False


def products_list_save_to_document(products_formset, document_instance, name_of_foreignkey_field: str):
    """
    Handles products form and links their instances to the document instance.
    """
    saved_product_instances = []
    for products_form in products_formset:
        if products_form.cleaned_data:
            products_instance = products_form.save(commit=False)
            setattr(products_instance, name_of_foreignkey_field, document_instance)
            products_instance.save()
            saved_product_instances.append(products_instance)
    return saved_product_instances


def add_department_to_products(product_instances: list, department):
    """
    Link product form to department from document
    """
    for product_instance in product_instances:
        product_instance.department = department
        product_instance.save()
        return product_instances


def get_next_document_number(model, numerator_field_name):
    """
    Check what is the last numerator field value in a model and determines the next one
    """
    last_number = model.objects.aggregate(Max(numerator_field_name))[f'{numerator_field_name}__max']
    if last_number is None:
        document_number = 1
    else:
        document_number = last_number + 1
    return document_number
