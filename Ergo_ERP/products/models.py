from django.db import models

# Create your models here.


class ProductsModel(models.Model):
    product_type_choices = [
        ('product', 'Product'),
        ('service', 'Service'),
        ('raw_material', 'Raw material'),
        ('part', 'Part')
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
    product_price_per_unit_with_vat = models.DecimalField(decimal_places=2, verbose_name='price')
    product_vat = models.DecimalField(decimal_places=2, verbose_name='vat')
    product_measuring_unit = models.CharField(max_length=10, verbose_name='unit', choices=product_measuring_unit_choices)
    product_notes = models.CharField(max_length=500)
    product_has_lot_and_exp_date = models.BooleanField()
    product_has_serial_number = models.BooleanField()
    product_recipie_or_parts_list = models.JSONField()
