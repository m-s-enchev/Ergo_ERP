from django.db import models


class ClientRepresentatives(models.Model):
    representative_names = models.CharField(max_length=50, verbose_name='names')
    representative_phone_number = models.CharField(max_length=15, verbose_name='phone_number', null=True, blank=True)
    representative_email = models.CharField(max_length=50, verbose_name='email', null=True, blank=True)
    representative_address = models.CharField(max_length=200, verbose_name='Address', null=True, blank=True)

    def __str__(self):
        return self.representative_names


class Clients(models.Model):
    client_names = models.CharField(max_length=50, verbose_name='names')
    client_phone_number = models.CharField(max_length=15, verbose_name='phone number', null=True, blank=True)
    client_email = models.CharField(max_length=50, verbose_name='email', null=True, blank=True)
    client_identification_number = models.CharField(max_length=20, verbose_name='identification number', null=True, blank=True)
    client_address = models.CharField(max_length=200, verbose_name='Address', null=True, blank=True)
    client_accountable_person = models.CharField(max_length=100, verbose_name='accountable person', null=True, blank=True)
    client_card_code = models.CharField(max_length=13, verbose_name='card barcode', blank=True, null=True)
    client_representatives = models.ForeignKey(ClientRepresentatives, on_delete=models.CASCADE, verbose_name='Representative', null=True, blank=True)

    def __str__(self):
        return self.client_names



