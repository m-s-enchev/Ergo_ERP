from django.db import models


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
    ingredient_manufacturer = models.CharField(max_length=100, verbose_name='manufacturer')
    ingredient_price_per_unit_with_vat = models.DecimalField(decimal_places=2, max_digits=10, verbose_name='price')
    ingredient_vat = models.DecimalField(decimal_places=2, max_digits=10, verbose_name='vat')
    ingredient_measuring_unit = models.CharField(
        max_length=20, verbose_name='unit',
        choices=ingredient_measuring_unit_choices
    )
    ingredient_has_lot_and_exp_date = models.BooleanField()


class ProductTags(models.Model):
    tag_name = models.CharField(max_length=100)


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
    product_category = models.CharField(max_length=100, verbose_name='category', blank=True, null=True)
    product_subcategory = models.CharField(max_length=100, verbose_name='subcategory', blank=True, null=True)
    # for UPC an EAN barcodes:
    product_barcode = models.CharField(max_length=13, verbose_name='barcode', blank=True, null=True)
    product_qrcode = models.CharField(max_length=100, verbose_name='QR code', blank=True, null=True)
    product_unit = models.CharField(max_length=20, verbose_name='unit', choices=product_measuring_unit_choices)
    product_notes = models.TextField(max_length=1000,  verbose_name='notes', blank=True, null=True)
    product_has_exp_date = models.BooleanField()
    product_made_in_department = models.CharField(
                                                    max_length=100,
                                                    verbose_name='manufacturing department',
                                                    blank=True,
                                                    null=True
                                                    )
    product_parts = models.ManyToManyField(IngredientOrPart, through='RecipeOrPartsList', verbose_name='parts', blank=True)
    product_tags = models.ManyToManyField(ProductTags, through='ProductTagList', verbose_name='tags', blank=True)
    # all prices are per unit before VAT
    product_vat = models.DecimalField(decimal_places=2, max_digits=10, default=0, verbose_name='VAT / Sales tax')
    product_retail_price = models.DecimalField(decimal_places=2, max_digits=10, verbose_name='retail price')
    product_wholesale_price = models.DecimalField(decimal_places=2, max_digits=10, verbose_name='wholesale price')
    product_employee_price = models.DecimalField(decimal_places=2, max_digits=10, verbose_name='employee price')


class RecipeOrPartsList (models.Model):
    product = models.ForeignKey(ProductsModel, on_delete=models.CASCADE)
    ingredient_or_part = models.ForeignKey(IngredientOrPart, on_delete=models.SET_NULL, null=True)
    ingredient_or_part_quantity = models.DecimalField(decimal_places=2, max_digits=10)


class ProductTagList (models.Model):
    product = models.ForeignKey(ProductsModel, on_delete=models.CASCADE)
    tag = models.ForeignKey(ProductTags, on_delete=models.SET_NULL, null=True)




