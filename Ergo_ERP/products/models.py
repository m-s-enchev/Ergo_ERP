from django.db import models

# Create your models here.


class IngredientOrPart (models.Model):
    ingredient_measuring_unit_choices = [
        ('pieces', 'pcs'),
        ('minutes', 'min'),
        ('hours', 'h'),
        ('grams', 'g'),
        ('kilograms', 'kg'),
        ('tons', 't'),
        ('milliliters', 'ml'),
        ('liters', 'l')
    ]

    ingredient_name = models.CharField(max_length=100)
    ingredient_measuring_unit = models.CharField(
        max_length=20, verbose_name='unit',
        choices=ingredient_measuring_unit_choices
    )
    ingredient_manufacturer = models.CharField(max_length=100, verbose_name='manufacturer')
    ingredient_price_per_unit_with_vat = models.DecimalField(decimal_places=2, max_digits=10, verbose_name='price')
    ingredient_vat = models.DecimalField(decimal_places=2, max_digits=10, verbose_name='vat')


class ProductRecipeOrPartsList (models.Model):
    ingredient_or_part = models.ForeignKey(IngredientOrPart, on_delete=models.CASCADE)
    ingredient_or_part_quantity = models.DecimalField(decimal_places=2, max_digits=10)





class ProductsModel(models.Model):
    product_type_choices = [
        ('product', 'Product'),
        ('service', 'Service'),
        ('voucher', 'Voucher'),
    ]

    product_measuring_unit_choices = [
        ('pieces', 'pcs'),
        ('minutes', 'min'),
        ('hours', 'h'),
        ('grams', 'g'),
        ('kilograms', 'kg'),
        ('tons', 't'),
        ('milliliters', 'ml'),
        ('liters', 'l')
    ]

    product_name = models.CharField(max_length=100, verbose_name='name')
    product_manufacturer = models.CharField(max_length=100, verbose_name='manufacturer')
    product_type = models.CharField(max_length=100, verbose_name='type', choices=product_type_choices)
    product_category = models.CharField(max_length=100, verbose_name='category')
    product_subcategory = models.CharField(max_length=100, verbose_name='subcategory')
    product_barcode = models.CharField(max_length=13, verbose_name='barcode')  # for UPC an EAN barcodes
    product_qrcode = models.CharField(max_length=100, verbose_name='QR code')
    product_price_per_unit_with_vat = models.DecimalField(decimal_places=2, max_digits=10, verbose_name='price')
    product_vat = models.DecimalField(decimal_places=2, max_digits=10, verbose_name='vat')
    product_unit = models.CharField(max_length=20, verbose_name='unit', choices=product_measuring_unit_choices)
    product_notes = models.CharField(max_length=500)
    product_has_lot_and_exp_date = models.BooleanField()
    product_has_serial_number = models.BooleanField()
    # product_recipie_or_parts_list = models.ForeignKey(ProductRecipeOrPartsList, on_delete=models.CASCADE)
    # В кой модел трябва да е ForeignKey?
    product_made_in_department = models.CharField(max_length=100, verbose_name='manufacturing department')


class ProductTags(models.Model):
    tag_name = models.CharField(max_length=100)
    tagged_product = models.ForeignKey(ProductsModel, on_delete=models.CASCADE)
