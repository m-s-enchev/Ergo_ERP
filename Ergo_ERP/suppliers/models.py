from django.db import models


class SupplierRepresentatives(models.Model):
    sup_represent_names = models.CharField(max_length=50, verbose_name='names')
    sup_represent_phone_number = models.CharField(max_length=15, verbose_name='phone_number', null=True, blank=True)
    sup_represent_email = models.CharField(max_length=50, verbose_name='email', null=True, blank=True)


class Suppliers(models.Model):
    supplier_name = models.CharField(max_length=50, verbose_name='names')
    supplier_phone_number = models.CharField(max_length=15, verbose_name='phone_number', null=True, blank=True)
    supplier_email = models.CharField(max_length=50, verbose_name='email', null=True, blank=True)
    supplier_identification_number = models.CharField(max_length=20, verbose_name='identification_number', null=True,
                                                      blank=True)
    supplier_address = models.CharField(max_length=200, verbose_name='Address', null=True, blank=True)
    supplier_accountable_person = models.CharField(max_length=100, verbose_name='accountable person', null=True,
                                                   blank=True)
    client_representatives = models.ForeignKey(SupplierRepresentatives, on_delete=models.CASCADE,
                                               verbose_name='Representative', null=True, blank=True)

    def __str__(self):
        return self.supplier_name
