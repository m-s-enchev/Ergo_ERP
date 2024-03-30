from django.contrib.auth.models import User
from django.db import models

from Ergo_ERP.clients.models import Clients
from Ergo_ERP.inventory.models import Department


class UserSettings(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    show_main_menu_shortcuts = models.BooleanField(null=True, blank=True)
    show_sale_quick_select = models.BooleanField(null=True, blank=True)
    default_sales_doc_is_invoice = models.BooleanField(null=True, blank=True)
    show_lot_and_exp_columns = models.BooleanField(null=True, blank=True)
    default_department = models.ForeignKey(Department, on_delete=models.CASCADE, null=True, blank=True)
    default_client = models.ForeignKey(Clients, on_delete=models.CASCADE, null=True, blank=True)

