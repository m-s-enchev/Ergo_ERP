from django.db import models


class Department(models.Model):
    name = models.CharField(max_length=30)
    location = models.CharField(max_length=255)

    def __str__(self):
        return self.name


class Inventory(models.Model):
    product_name = models.CharField(max_length=100, verbose_name='name')
    product_quantity = models.DecimalField(decimal_places=2, max_digits=10, verbose_name='Qty')
    product_unit = models.CharField(max_length=20, verbose_name='Unit')
    product_lot_number = models.CharField(max_length=100, verbose_name='LOT', null=True, blank=True)
    product_exp_date = models.DateField(verbose_name='Exp. date', null=True, blank=True, )
    # price and value are before TAX
    product_purchase_price = models.DecimalField(decimal_places=2, max_digits=10, verbose_name='Price',
                                                 null=True, blank=True)
    product_value = models.DecimalField(decimal_places=2, max_digits=10, verbose_name='Price',
                                        null=True, blank=True)
    department = models.ForeignKey(Department, on_delete=models.CASCADE, null=True, blank=True)


class WarehouseDocument(models.Model):
    date = models.DateField()
    time = models.TimeField(auto_now_add=True)
    operator = models.CharField(max_length=100, null=True, blank=True)
    total_sum = models.DecimalField(decimal_places=2, max_digits=10, verbose_name='Total', null=True, blank=True)

    class Meta:
        abstract = True


class ReceivingDocument(WarehouseDocument):
    shipping_department = models.CharField(max_length=100)
    receiving_department = models.ForeignKey(Department, on_delete=models.CASCADE, null=True, blank=True)
    receiving = True


class ShippingDocument(WarehouseDocument):
    shipping_department = models.ForeignKey(Department, on_delete=models.CASCADE, null=True, blank=True)
    receiving_department = models.CharField(max_length=100)
    receiving = False


class TransferredProducts(models.Model):
    product_name = models.CharField(max_length=200, verbose_name='Name')
    product_quantity = models.DecimalField(decimal_places=2, max_digits=10, verbose_name='Qty')
    product_unit = models.CharField(max_length=20, verbose_name='Unit')
    product_lot_number = models.CharField(max_length=100, verbose_name='LOT', null=True, blank=True)
    product_exp_date = models.DateField(verbose_name='Exp. date', null=True, blank=True)
    product_purchase_price = models.DecimalField(decimal_places=2, max_digits=10, verbose_name='Purchase price',
                                                 null=True, blank=True)
    product_value = models.DecimalField(decimal_places=2, max_digits=10, verbose_name='Amount', null=True, blank=True)
    department = models.ForeignKey(Department, on_delete=models.CASCADE, null=True, blank=True)

    class Meta:
        abstract = True


class ReceivedProducts(TransferredProducts):
    linked_warehouse_document = models.ForeignKey(ReceivingDocument, on_delete=models.CASCADE)


class ShippedProducts(TransferredProducts):
    linked_warehouse_document = models.ForeignKey(ShippingDocument, on_delete=models.CASCADE)
