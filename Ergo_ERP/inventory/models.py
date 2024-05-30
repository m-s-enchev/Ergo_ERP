from django.contrib.auth.models import User
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
    product_purchase_price = models.DecimalField(decimal_places=2, max_digits=10, verbose_name='Price')
    product_total = models.DecimalField(decimal_places=2, max_digits=10, verbose_name='Price')
    department = models.ForeignKey(Department, on_delete=models.CASCADE)


class WarehouseDocument(models.Model):
    date = models.DateField()
    time = models.TimeField(auto_now_add=True)
    total_sum = models.DecimalField(decimal_places=2, max_digits=10, verbose_name='Total')
    operator = models.ForeignKey(User, on_delete=models.CASCADE)

    class Meta:
        abstract = True


class ReceivingDocument(WarehouseDocument):
    shipping_department = models.ForeignKey(Department, on_delete=models.CASCADE, related_name='receiving_from')
    receiving_department = models.ForeignKey(Department, on_delete=models.CASCADE, related_name='receiving_to')
    receiving = True


class ShippingDocument(WarehouseDocument):
    shipping_department = models.ForeignKey(Department, on_delete=models.CASCADE, related_name='shipping_from')
    receiving_department = models.ForeignKey(Department, on_delete=models.CASCADE, related_name='shipping_to')
    receiving = False


class TransferredProducts(models.Model):
    product_name = models.CharField(max_length=200, verbose_name='Name')
    product_quantity = models.DecimalField(decimal_places=2, max_digits=10, verbose_name='Qty')
    product_unit = models.CharField(max_length=20, verbose_name='Unit')
    product_lot_number = models.CharField(max_length=100, verbose_name='LOT', null=True, blank=True)
    product_exp_date = models.DateField(verbose_name='Exp. date', null=True, blank=True)
    product_purchase_price = models.DecimalField(decimal_places=2, max_digits=10, verbose_name='Purchase price')
    product_total = models.DecimalField(decimal_places=2, max_digits=10, verbose_name='Amount')
    department = models.ForeignKey(Department, on_delete=models.CASCADE)

    class Meta:
        abstract = True


class ReceivedProducts(TransferredProducts):
    linked_warehouse_document = models.ForeignKey(ReceivingDocument, on_delete=models.CASCADE)


class ShippedProducts(TransferredProducts):
    linked_warehouse_document = models.ForeignKey(ShippingDocument, on_delete=models.CASCADE)
