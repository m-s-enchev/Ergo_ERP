from django.db import models


class Inventory (models.Model):
    product_name = models.CharField(max_length=100, verbose_name='name')
    product_quantity = models.DecimalField(decimal_places=2, max_digits=10, verbose_name='Qty')
    product_lot_number = models.CharField(max_length=100, verbose_name='LOT', null=True, blank=True)
    product_exp_date = models.DateField(verbose_name='Exp. date', null=True, blank=True, )
    product_purchase_price = models.DecimalField(decimal_places=2, max_digits=10, verbose_name='Price', null=True, blank=True)
