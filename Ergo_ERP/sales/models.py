from django.db import models

# Create your models here.


class SoldProducts (models.Model):
    product = models.CharField(max_length=200)
    product_quantity = models.FloatField(verbose_name='Qty')
    product_price_before_tax = models.DecimalField('Price before VAT')
    product_price = models.DecimalField(verbose_name='Price')
    product_discount = models.DecimalField(verbose_name='Discount')
    product_total_before_tax = models.DecimalField('Amount before VAT')
    product_total = models.DecimalField(verbose_name='Amount')
    product_lot_number = models.CharField(max_length=100, verbose_name='LOT')
    product_exp_date = models.DateField(verbose_name='Exp. date')


class SalesDocument(models.Model):
    date = models.DateField(auto_now_add=True)
    time = models.TimeField(auto_now_add=True)
    operator = models.CharField(max_length=100)
    department = models.CharField(max_length=100)
    warehouse = models.CharField(max_length=100)
    seller_name = models.CharField(max_length=100, verbose_name='Seller')
    seller_identification_number = models.CharField(max_length=20, verbose_name='Identification number')
    seller_address = models.CharField(max_length=200, verbose_name='Address')
    seller_accountable_person = models.CharField(max_length=100, verbose_name='accountable person')
    seller_iban = models.CharField(max_length=34, verbose_name='IBAN')
    seller_representative = models.CharField(max_length=100)
    buyer_name = models.CharField(max_length=100, verbose_name='Buyer')
    buyer_identification_number = models.CharField(max_length=20, verbose_name='Identification number')
    buyer_address = models.CharField(max_length=200, verbose_name='Address')
    buyer_accountable_person = models.CharField(max_length=100, verbose_name='accountable person')
    buyer_representative = models.CharField(max_length=100, verbose_name='representative')
    sale_total_before_tax = models.DecimalField(verbose_name='Subtotal')
    sale_total_tax = models.DecimalField(verbose_name='VAT')
    sale_total_final = models.DecimalField(verbose_name='TOTAL')
    payment_method = models.CharField(max_length=30)
    due_date = models.DateField()
    products_sold = models.ForeignKey(SoldProducts, on_delete=models.CASCADE)








