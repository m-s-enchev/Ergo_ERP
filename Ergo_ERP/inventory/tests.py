from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.test import TestCase
from django.forms import Form
from unittest.mock import MagicMock

from django.urls import reverse

from .models import Inventory, Department, ReceivingDocument, ReceivedProducts, ShippingDocument, ShippedProducts
from .helper_functions import check_inventory, create_inventory_instance, receive_in_inventory, subtract_from_inventory, \
    update_inventory


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


class CreateInventoryInstanceTest(TestCase):
    def setUp(self):
        self.department_receive = Department.objects.create(name='Store', location='Sofia')
        self.department_ship = Department.objects.create(name='Warehouse', location='Plovdiv')
        self.user = User.objects.create(username='test_user', password='test_password')
        self.receiving_document = ReceivingDocument.objects.create(
            date='2025-05-05',
            time='22:19:55',
            total_sum=55.44,
            operator=self.user,
            shipping_department=self.department_ship,
            receiving_department=self.department_receive,
        )

        self.product_instance = ReceivedProducts.objects.create(
            product_name='Bucket',
            product_quantity=10,
            product_unit='pieces',
            product_purchase_price=10,
            product_total=100,
            department=self.department_receive,
            linked_warehouse_document=self.receiving_document
        )

    def test_creates_new_inventory_instance_successfully(self):
        create_inventory_instance(self.product_instance)
        self.assertTrue(Inventory.objects.all().count(), 1)


class ReceiveInInventoryTest(TestCase):
    def setUp(self):
        self.matching_name = 'Bucket'
        self.matching_lot_number = 'L123'
        self.department_ship = Department.objects.create(name='Warehouse', location='Plovdiv')
        self.department_receive = Department.objects.create(name='Store', location='Sofia')
        self.user = User.objects.create(username='test_user', password='test_password')

        self.receiving_document = ReceivingDocument.objects.create(
            date='2025-04-05',
            time='22:19:56',
            total_sum=55.30,
            operator=self.user,
            shipping_department=self.department_ship,
            receiving_department=self.department_receive,
        )
        self.product_instance = ReceivedProducts.objects.create(
            product_name=self.matching_name,
            product_quantity=10,
            product_unit='pieces',
            product_lot_number=self.matching_lot_number,
            product_purchase_price=10,
            product_total=100,
            department=self.department_receive,
            linked_warehouse_document=self.receiving_document
        )

    def test_receive_in_inventory_existing_product_and_lot(self):
        self.matching_inventory_instance = Inventory.objects.create(
            product_name=self.matching_name,
            product_unit='pieces',
            product_lot_number=self.matching_lot_number,
            department=self.department_receive,
            product_quantity=5,
            product_purchase_price=2,
            product_total=10
        )
        receive_in_inventory(self.matching_inventory_instance, self.product_instance)
        self.assertEqual(self.matching_inventory_instance.product_quantity, 15)
        self.assertEqual(self.matching_inventory_instance.product_total, 110)
        self.assertEqual(
            self.matching_inventory_instance.purchase_price,
            (self.matching_inventory_instance.product_total/self.matching_inventory_instance.product_quantity)
        )

    def test_receive_in_inventory_create_new_instance(self):
        self.product_instance.product_name = 'New product'
        receive_in_inventory(None, self.product_instance)
        self.assertEqual(Inventory.objects.all().count(), 1)
        self.assertEqual(Inventory.objects.first().product_name, 'New product')



class SubtractFromInventoryTest(TestCase):
    def setUp(self):
        self.matching_name = 'Socket'
        self.matching_lot_number = 'L123'
        self.department_ship = Department.objects.create(name='Warehouse', location='Plovdiv')
        self.department_receive = Department.objects.create(name='Store', location='Sofia')
        self.user = User.objects.create(username='test_user', password='test_password')
        self.matching_inventory_instance = Inventory.objects.create(
            product_name=self.matching_name,
            product_unit='pieces',
            product_lot_number=self.matching_lot_number,
            department=self.department_receive,
            product_quantity=50,
            product_purchase_price=5,
            product_total=250
        )
        self.shipping_document = ShippingDocument.objects.create(
            date='2024-04-05',
            time='22:19:56',
            total_sum=55.30,
            operator=self.user,
            shipping_department=self.department_ship,
            receiving_department=self.department_receive,
        )
        self.product_instance = ShippedProducts.objects.create(
            product_name=self.matching_name,
            product_quantity=10,
            product_unit='pieces',
            product_lot_number=self.matching_lot_number,
            product_purchase_price=5,
            product_total=50,
            department=self.department_ship,
            linked_warehouse_document=self.shipping_document
        )

    def test_ship_from_inventory_with_enough_quantity(self):
        subtract_from_inventory(self.matching_inventory_instance, self.product_instance)
        self.assertEqual(self.matching_inventory_instance.product_quantity, 40)
        self.assertEqual(self.matching_inventory_instance.product_total, 200)
        self.assertEqual(
            self.matching_inventory_instance.product_purchase_price,
            (self.matching_inventory_instance.product_total/self.matching_inventory_instance.product_quantity)
        )

    def test_subtract_from_inventory_validation_error(self):
        self.matching_inventory_instance.product_quantity = 5
        with self.assertRaises(ValidationError) as context:
            subtract_from_inventory(self.matching_inventory_instance, self.product_instance)
        self.assertEqual(
            str(context.exception),
            "['There is not enough of product Socket with lot L123.']"
        )


class UpdateInventoryTest(TestCase):
    def setUp(self):
        self.matching_name = 'Mop'
        self.matching_lot_number = 'L123'
        self.department_ship = Department.objects.create(name='Warehouse', location='Plovdiv')
        self.department_receive = Department.objects.create(name='Store', location='Sofia')
        self.user = User.objects.create(username='test_user', password='test_password')
        self.receiving_document = ReceivingDocument.objects.create(
            date='2025-04-05',
            time='22:19:56',
            total_sum=55.20,
            operator=self.user,
            shipping_department=self.department_ship,
            receiving_department=self.department_receive,
        )
        self.product_instance_received_1 = ReceivedProducts.objects.create(
            product_name=self.matching_name,
            product_quantity=50,
            product_unit='pieces',
            product_lot_number=self.matching_lot_number,
            product_purchase_price=5,
            product_total=250,
            department=self.department_receive,
            linked_warehouse_document=self.receiving_document
        )

        self.product_instance_received_2 = ReceivedProducts.objects.create(
            product_name='Different name',
            product_quantity=10,
            product_unit='pieces',
            product_lot_number=self.matching_lot_number,
            product_purchase_price=3,
            product_total=30,
            department=self.department_receive,
            linked_warehouse_document=self.receiving_document
        )

        self.shipping_document = ShippingDocument.objects.create(
            date='2024-04-05',
            time='22:18:56',
            total_sum=55.30,
            operator=self.user,
            shipping_department=self.department_ship,
            receiving_department=self.department_receive,
        )

        self.product_instance_shipped_1 = ShippedProducts.objects.create(
            product_name=self.matching_name,
            product_quantity=4,
            product_unit='pieces',
            product_lot_number=self.matching_lot_number,
            product_purchase_price=5,
            product_total=20,
            department=self.department_ship,
            linked_warehouse_document=self.shipping_document
        )

        self.product_instance_shipped_2 = ShippedProducts.objects.create(
            product_name='New product',
            product_quantity=5,
            product_unit='pieces',
            product_lot_number=self.matching_lot_number,
            product_purchase_price=4,
            product_total=20,
            department=self.department_ship,
            linked_warehouse_document=self.shipping_document
        )

        self.matching_inventory_instance = Inventory.objects.create(
            product_name=self.matching_name,
            product_unit='pieces',
            product_lot_number=self.matching_lot_number,
            department=self.department_receive,
            product_quantity=10,
            product_purchase_price=5,
            product_total=50
        )

    def test_receiving_two_products_one_matches(self):
        self.product_instances_receiving = [self.product_instance_received_1, self.product_instance_received_2]
        update_inventory(self.product_instances_receiving, True, self.department_receive)
        self.assertEqual(Inventory.objects.all().count(), 2)
        self.assertEqual(Inventory.objects.first().product_quantity, 60)
        self.assertEqual(Inventory.objects.first().product_total, 300)
        self.assertEqual(Inventory.objects.first().product_purchase_price, 5.00)

    def test_receiving_two_products_no_matches(self):
        self.product_instance_received_1.product_name = 'Canu'
        self.product_instances_receiving = [self.product_instance_received_1, self.product_instance_received_2]
        update_inventory(self.product_instances_receiving, True, self.department_receive)
        self.assertEqual(Inventory.objects.all().count(), 3)

    def test_shipping_a_product(self):
        self.product_instances_shipping = [self.product_instance_shipped_1]
        self.matching_inventory_instance.department = self.department_ship
        self.matching_inventory_instance.save()
        update_inventory(self.product_instances_shipping, False, self.department_ship)
        self.assertEqual(Inventory.objects.all().count(), 1)
        self.assertEqual(Inventory.objects.first().product_quantity, 6)
        self.assertEqual(Inventory.objects.first().product_total, 30)
        self.assertEqual(Inventory.objects.first().product_purchase_price, 5.00)


class HandleReceivingDocumentFormsTest(TestCase):
    def setUp(self):

        self.department_receive = Department.objects.create(name='Store', location='Sofia')
        self.department_ship = Department.objects.create(name='Warehouse', location='Plovdiv')
        self.user = User.objects.create(username='test_user', password='test_password')
        self.receiving_document_form = MagicMock(
            date='2025-05-05',
            time='22:19:55',
            total_sum=55.44,
            operator=self.user,
            shipping_department=self.department_ship,
            receiving_department=self.department_receive,
        )

        self.product_instance = ReceivedProducts.objects.create(
            product_name='Bucket',
            product_quantity=10,
            product_unit='pieces',
            product_purchase_price=10,
            product_total=100,
            department=self.department_receive,
            linked_warehouse_document=self.receiving_document
        )

# -------------------- TEST Views -----------------------


class InventoryViewTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='password')
        self.client.login(username='testuser', password='password')
        self.first_matching_name = 'Bucket'
        self.second_matching_name = 'Socket'
        self.department = Department.objects.create(name='Warehouse', location='Plovdiv')
        self.first_inventory_instance = Inventory.objects.create(
            product_name=self.first_matching_name,
            product_unit='pieces',
            product_lot_number='L123',
            department=self.department,
            product_quantity=10,
            product_purchase_price=5,
            product_total=50
        )

        self.second_inventory_instance = Inventory.objects.create(
            product_name='Mop',
            product_unit='pieces',
            product_lot_number='L456',
            department=self.department,
            product_quantity=10,
            product_purchase_price=5,
            product_total=50
        )

    def test_get_queryset_one_match(self):
        response = self.client.get(reverse('inventory'), {'search_query': 'Buck', 'department': self.department})
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Bucket')
        self.assertNotContains(response, 'Mop')

    def test_get_queryset_two_matches(self):
        self.second_inventory_instance.product_name = self.second_matching_name
        self.second_inventory_instance.save()
        response = self.client.get(reverse('inventory'), {'search_query': 'cket', 'department': self.department})
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Bucket')
        self.assertContains(response, 'Socket')

    def test_get_queryset_no_search_query_no_department(self):
        response = self.client.get(reverse('inventory'), {'search_query': '', 'department': ''})
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Bucket')
        self.assertContains(response, 'Mop')

    def test_get_queryset_no_search_query_with_department(self):
        response = self.client.get(reverse('inventory'), {'search_query': '', 'department': self.department})
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Bucket')
        self.assertContains(response, 'Mop')

    def test_get_context_data(self):
        response = self.client.get(reverse('inventory'))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.context['departments']), 1)
        self.assertIn(self.department, response.context['departments'])
