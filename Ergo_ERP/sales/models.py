from django.db import models


class SalesDocument(models.Model):
    payment_method_choices = [
        ('cash', 'cash'),
        ('card', 'card'),
        ('wire_transfer', 'wire transfer'),
        ('add_to_bill', 'add to bill')
    ]
    date = models.DateField()
    time = models.TimeField(auto_now_add=True)
    operator = models.CharField(max_length=100)
    department = models.CharField(max_length=100)
    warehouse = models.CharField(max_length=100)
    buyer_name = models.CharField(max_length=100, verbose_name='Client')
    sale_total_before_tax = models.DecimalField(null=True, blank=True, decimal_places=2, max_digits=10, verbose_name='Subtotal')
    sale_total_tax = models.DecimalField(null=True,  blank=True,decimal_places=2, max_digits=10, verbose_name='VAT')
    sale_total_final = models.DecimalField(null=True,  blank=True,decimal_places=2, max_digits=10, verbose_name='TOTAL')
    payment_method = models.CharField(null=True, blank=True, max_length=30)
    is_linked_to_invoice = models.BooleanField(default=False)


class SoldProductsBaseModel(models.Model):
    product_name = models.CharField(max_length=200, verbose_name='Name')
    product_quantity = models.DecimalField(decimal_places=2, max_digits=10, verbose_name='Qty')
    product_price_before_tax = models.DecimalField(decimal_places=2, max_digits=10, verbose_name='Price before VAT',
                                                   null=True, blank=True)
    product_price = models.DecimalField(decimal_places=2, max_digits=10, verbose_name='Price', null=True, blank=True)
    product_discount = models.DecimalField(decimal_places=2, max_digits=10, verbose_name='Discount', null=True,
                                           blank=True)
    product_total_before_tax = models.DecimalField(decimal_places=2, max_digits=10, verbose_name='Amount before VAT',
                                                   null=True, blank=True)
    product_total = models.DecimalField(decimal_places=2, max_digits=10, verbose_name='Amount', null=True, blank=True)
    product_lot_number = models.CharField(max_length=100, verbose_name='LOT', null=True, blank=True)
    product_exp_date = models.DateField(verbose_name='Exp. date', null=True, blank=True, )

    class Meta:
        abstract = True

    def __str__(self):
        return self.product_name


class SoldProducts (SoldProductsBaseModel):
    sales_document_in_which_sold = models.ForeignKey(SalesDocument, on_delete=models.CASCADE)


class InvoiceData(models.Model):
    invoice_number = models.IntegerField(verbose_name='Number')
    invoice_date = models.DateField(verbose_name='Date')
    invoice_due_date = models.DateField(verbose_name='Due date')
    buyer_identification_number = models.CharField(max_length=20, verbose_name='Identification number')
    buyer_address = models.CharField(max_length=200, verbose_name='Address')
    buyer_accountable_person = models.CharField(max_length=100, verbose_name='accountable person')
    buyer_representative = models.CharField(max_length=100, verbose_name='representative')
    sales_document_for_invoice = models.OneToOneField(SalesDocument, on_delete=models.CASCADE)


class InvoicedProducts (SoldProductsBaseModel):
    invoice_document_in_which_included = models.ForeignKey(InvoiceData, on_delete=models.CASCADE)

    @staticmethod
    def get_fields_to_copy():
        return [
                'product_name',
                'product_quantity',
                'product_price_before_tax',
                'product_price',
                'product_discount',
                'product_total_before_tax',
                'product_total',
                'product_lot_number',
                'product_exp_date'
                ]


# seller_name = models.CharField(max_length=100, verbose_name='Seller')
# seller_identification_number = models.CharField(max_length=20, verbose_name='Identification number')
# seller_address = models.CharField(max_length=200, verbose_name='Address')
# seller_accountable_person = models.CharField(max_length=100, verbose_name='accountable person')
# seller_iban = models.CharField(max_length=34, verbose_name='IBAN')
# seller_representative = models.CharField(null=True, blank=True, max_length=100)


