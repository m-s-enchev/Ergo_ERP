from django.db import models


class Inventory(models.Model):
    product_name = models.CharField(max_length=100, verbose_name='name')
    product_quantity = models.DecimalField(decimal_places=2, max_digits=10, verbose_name='Qty')
    product_lot_number = models.CharField(max_length=100, verbose_name='LOT', null=True, blank=True)
    product_exp_date = models.DateField(verbose_name='Exp. date', null=True, blank=True, )
    product_purchase_price = models.DecimalField(decimal_places=2, max_digits=10, verbose_name='Price',
                                                 null=True, blank=True)
    product_value = models.DecimalField(decimal_places=2, max_digits=10, verbose_name='Price',
                                        null=True, blank=True)


class WarehouseDocument(models.Model):
    """
    For both receiving and sending goods
    """
    date = models.DateField()
    time = models.TimeField(auto_now_add=True)
    operator = models.CharField(max_length=100)
    shipping_department = models.CharField(max_length=100)
    shipping_warehouse = models.CharField(max_length=100)
    receiving_department = models.CharField(max_length=100)
    receiving_warehouse = models.CharField(max_length=100)
    total_sum = models.DecimalField(decimal_places=2, max_digits=10, verbose_name='Total',
                                    null=True, blank=True, )
    receiving = models.BooleanField(default=False)


class TransferredProducts(models.Model):
    product_name = models.CharField(max_length=200, verbose_name='Name')
    product_quantity = models.DecimalField(decimal_places=2, max_digits=10, verbose_name='Qty')
    product_lot_number = models.CharField(max_length=100, verbose_name='LOT', null=True, blank=True)
    product_exp_date = models.DateField(verbose_name='Exp. date', null=True, blank=True, )
    product_purchase_price = models.DecimalField(decimal_places=2, max_digits=10, verbose_name='Purchase price',
                                                 null=True, blank=True)
    product_value = models.DecimalField(decimal_places=2, max_digits=10,
                                        null=True, blank=True)
    warehouse_document_in_which_included = models.ForeignKey(WarehouseDocument, on_delete=models.CASCADE)
