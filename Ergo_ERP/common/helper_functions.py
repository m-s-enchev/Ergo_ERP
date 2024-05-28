from django.db.models import Max


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
