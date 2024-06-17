from datetime import datetime
from unittest import TestCase
from unittest.mock import MagicMock, patch

from _decimal import Decimal

from Ergo_ERP.common.helper_functions import is_formset_nonempty, products_list_save_to_document, \
    get_next_document_number, inventory_products_dict, products_all_dict, check_product_name, products_names_list
from Ergo_ERP.inventory.models import Inventory, Department
from Ergo_ERP.products.models import ProductsModel


# -------------------- TEST Helper Functions-----------------------

class IsFormsetNonemptyTest(TestCase):
    def setUp(self):
        self.form1 = MagicMock()
        self.form1.cleaned_data = {'name': 'Bucket', 'quantity': 1}
        self.form2 = MagicMock()
        self.form2.cleaned_data = {}
        self.formset = [self.form1, self.form2]

    def test_formset_is_empty(self):
        self.form1.cleaned_data = {}
        self.assertFalse(is_formset_nonempty(self.formset))

    def test_formset_with_one_non_empty(self):
        self.assertTrue(is_formset_nonempty(self.formset))

    def test_formset_with_all_non_empty(self):
        self.form2.cleaned_data = {'name': 'Socket', 'quantity': 5}
        self.assertTrue(is_formset_nonempty(self.formset))


class ProductsListSaveToDocumentTest(TestCase):
    def setUp(self):
        self.document_instance = MagicMock()
        self.document_instance.id = 1

    def test_document_no_department(self):
        form1 = MagicMock()
        form1.cleaned_data = {'name': 'Bucket', 'quantity': 1, 'sales_document': ''}
        form1.save.side_effect = [form1, form1]

        form2 = MagicMock()
        form2.cleaned_data = {'name': 'Socket', 'quantity': 2, 'sales_document': ''}
        form2.save.side_effect = [form2, form2]

        formset = [form1, form2]

        with patch('Ergo_ERP.common.helper_functions.DatabaseError', Exception):
            saved_product_instances = products_list_save_to_document(formset, self.document_instance, 'sales_document')

        self.assertEqual(len(saved_product_instances), 2)
        self.assertEqual(saved_product_instances[0].cleaned_data['name'], 'Bucket')
        self.assertEqual(saved_product_instances[0].cleaned_data['quantity'], 1)
        self.assertEqual(saved_product_instances[1].cleaned_data['name'], 'Socket')
        self.assertEqual(saved_product_instances[1].cleaned_data['quantity'], 2)
        self.assertEqual(form1.save.call_count, 2)
        self.assertEqual(form2.save.call_count, 2)


class GetNextDocumentNumberTest(TestCase):
    def setUp(self):
        self.model = MagicMock()
        self.model.objects.aggregate.return_value = {'numerator_field_name__max': 1}

    def test_no_last_number(self):
        self.model.objects.aggregate.return_value = {'numerator_field_name__max': None}
        self.assertEqual(get_next_document_number(self.model, 'numerator_field_name'), 1)

    def test_last_number(self):
        self.assertEqual(get_next_document_number(self.model, 'numerator_field_name'), 2)


class InventoryProductsDictTest(TestCase):
    def setUp(self):
        self.department_1 = MagicMock(spec=Department, name='Test Department 1')
        self.department_2 = MagicMock(spec=Department, name='Test Department 2')

        self.first_inventory_instance = MagicMock(
            sepc=Inventory,
            product_name='Bucket',
            product_unit='pieces',
            product_lot_number='123',
            product_exp_date=datetime.strptime('2021-01-01', '%Y-%m-%d'),
            department=self.department_1,
            product_quantity=Decimal('10'),
            product_purchase_price=Decimal('5'),
            product_total=Decimal('50')
        )

        self.second_inventory_instance = MagicMock(
            sepc=Inventory,
            product_name='Socket',
            product_unit='pieces',
            product_lot_number='456',
            product_exp_date=datetime.strptime('2023-03-03', '%Y-%m-%d'),
            department=self.department_2,
            product_quantity=Decimal('5'),
            product_purchase_price=Decimal('2'),
            product_total=Decimal('10')
        )

    @patch('Ergo_ERP.common.helper_functions.Inventory.objects.all')
    def test_no_department(self, inventory_objects_all):
        inventory_objects_all.return_value = [self.first_inventory_instance, self.second_inventory_instance]
        self.assertEqual(len(inventory_products_dict()), 2)
        self.assertEqual(inventory_products_dict()['Bucket'], ['10', 'pieces', '123', '01.01.2021'])
        self.assertEqual(inventory_products_dict()['Socket'], ['5', 'pieces', '456', '03.03.2023'])

    @patch('Ergo_ERP.common.helper_functions.Inventory.objects.filter')
    def test_with_department(self, inventory_objects_filter):
        inventory_objects_filter.return_value = [self.first_inventory_instance]
        self.assertEqual(len(inventory_products_dict(self.department_1)), 1)
        self.assertEqual(inventory_products_dict(self.department_1)['Bucket'], ['10', 'pieces', '123', '01.01.2021'])

    @patch('Ergo_ERP.common.helper_functions.Inventory.objects.all')
    def test_with_no_exp_date(self, inventory_objects_all):
        self.first_inventory_instance.product_exp_date = None
        inventory_objects_all.return_value = [self.first_inventory_instance, self.second_inventory_instance]
        self.assertEqual(len(inventory_products_dict()), 2)
        self.assertEqual(inventory_products_dict()['Bucket'], ['10', 'pieces', '', ''])


class ProductsAllDictTest(TestCase):
    def setUp(self):
        self.first_product = MagicMock(
            spec=ProductsModel,
            product_name='Bucket',
            product_unit='pieces'
        )

        self.second_product = MagicMock(
            spec=ProductsModel,
            product_name='Socket',
            product_unit='pieces'
        )

    @patch('Ergo_ERP.common.helper_functions.ProductsModel.objects.all')
    def test_products_all_dict(self, products):
        products.return_value = [self.first_product, self.second_product]
        self.assertEqual(len(products_all_dict()), 2)
        self.assertEqual(products_all_dict()['Bucket'], 'pieces')
        self.assertEqual(products_all_dict()['Socket'], 'pieces')


class CheckProductNameTest(TestCase):
    def setUp(self):
        self.valid_form = MagicMock()
        self.valid_form.cleaned_data = {'product_name': 'Bucket'}
        self.invalid_form = MagicMock()
        self.invalid_form.cleaned_data = {'product_name': 'Coke'}

    @patch('Ergo_ERP.common.helper_functions.ProductsModel.objects.filter')
    def test_product_is_valid(self, mock_filter):
        mock_filter.return_value.exists.return_value = True
        products_formset = [self.valid_form]
        self.assertTrue(check_product_name(products_formset))
        mock_filter.assert_called_once_with(product_name='Bucket')

    @patch('Ergo_ERP.common.helper_functions.ProductsModel.objects.filter')
    def test_product_is_not_valid(self, mock_filter):
        mock_filter.return_value.exists.return_value = False
        products_formset = [self.invalid_form]
        self.assertFalse(check_product_name(products_formset))
        mock_filter.assert_called_once_with(product_name='Coke')
        self.invalid_form.add_error.assert_called_once_with('product_name', "No such product!")


class ProductsNamesListTest(TestCase):
    def setUp(self):
        self.first_product = MagicMock(
            spec=ProductsModel,
            product_name='Bucket',
            product_unit='pieces'
        )
        self.second_product = MagicMock(
            spec=ProductsModel,
            product_name='Socket',
            product_unit='pieces'
        )

    @patch('Ergo_ERP.common.helper_functions.ProductsModel.objects.all')
    def test_products_all_dict(self, products):
        products.return_value = [self.first_product, self.second_product]
        returned_list = products_names_list()
        self.assertEqual(len(returned_list), 2)
        self.assertEqual(returned_list[0], 'Bucket')
        self.assertEqual(returned_list[1], 'Socket')



