from django.test import TestCase
from django.forms import Form
from unittest.mock import MagicMock
from .models import Inventory, Department
from .helper_functions import check_inventory

# -------------------- TEST Helper Functions-----------------------


class CheckInventoryTest(TestCase):

    def setUp(self):
        self.department = Department.objects.create(name='Warehouse', location='Sofia')
        self.first_product_name = 'Product 1'
        self.second_product_name = 'Product 2'
        self.first_product_lot = 'Lot123'
        self.second_product_lot = 'Lot456'

        self.first_inventory_instance = Inventory.objects.create(
                                            product_name=self.first_product_name,
                                            product_unit='pieces',
                                            product_lot_number=self.first_product_lot,
                                            department=self.department,
                                            product_quantity=10,
                                            product_purchase_price=5,
                                            product_total=50
                                        )
        self.second_inventory_instance = Inventory.objects.create(
                                            product_name=self.second_product_name,
                                            product_unit='pieces',
                                            product_lot_number=self.second_product_lot,
                                            department=self.department,
                                            product_quantity=5,
                                            product_purchase_price=2,
                                            product_total=10
                                        )

        self.document_form = MagicMock()
        self.document_form.cleaned_data = {'department': self.department}

        self.first_product_form = MagicMock(spec=Form)
        self.first_product_form.cleaned_data = {
            'product_name': self.first_product_name,
            'product_unit': 'pieces',
            'product_lot_number': self.first_product_lot,
            'product_quantity': 10,
        }

        self.products_formset = [self.first_product_form]

    def test_product_lot_exist_sufficient_quantity(self):
        self.first_inventory_instance.product_quantity = 15
        self.first_inventory_instance.save()
        all_valid = check_inventory(self.document_form, self.products_formset)
        self.assertTrue(all_valid)
        self.first_product_form.add_error.assert_not_called()

    def test_product_lot_exist_insufficient_quantity(self):
        self.first_inventory_instance.product_quantity = 5
        self.first_inventory_instance.save()
        all_valid = check_inventory(self.document_form, self.products_formset)
        self.assertFalse(all_valid)
        self.first_product_form.add_error.assert_called_once_with('product_quantity', "Insufficient quantity !")

    def test_product_lot_does_not_exist(self):
        self.first_inventory_instance.delete()
        all_valid = check_inventory(self.document_form, self.products_formset)
        self.assertFalse(all_valid)
        self.first_product_form.add_error.assert_called_once_with('product_name', "No such product or lot !")

    def test_product_lot_exists_exact_quantity(self):
        all_valid = check_inventory(self.document_form, self.products_formset)
        self.assertTrue(all_valid)
        self.first_product_form.add_error.assert_not_called()

    def test_multiple_products_all_valid(self):
        second_product_form = MagicMock(spec=Form)
        second_product_form.cleaned_data = {
            'product_name': self.second_product_name,
            'product_unit': 'pieces',
            'product_lot_number': self.second_product_lot,
            'product_quantity': 3,
        }
        self.products_formset.append(second_product_form)
        all_valid = check_inventory(self.document_form, self.products_formset)
        self.assertTrue(all_valid)
        self.first_product_form.add_error.assert_not_called()
        second_product_form.add_error.assert_not_called()

    def test_multiple_products_one_invalid(self):
        second_product_form = MagicMock(spec=Form)
        second_product_form.cleaned_data = {
            'product_name': self.second_product_name,
            'product_unit': 'pieces',
            'product_lot_number': self.second_product_lot,
            'product_quantity': 6
        }
        self.products_formset.append(second_product_form)
        all_valid = check_inventory(self.document_form, self.products_formset)
        self.assertFalse(all_valid)
        self.first_product_form.add_error.assert_not_called()
        second_product_form.add_error.assert_called_once_with('product_quantity', "Insufficient quantity !")






