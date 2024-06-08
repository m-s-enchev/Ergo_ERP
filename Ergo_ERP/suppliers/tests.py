from django.test import TestCase, RequestFactory
from django.urls import reverse
from django.contrib.auth.models import User
from .models import Suppliers
from .views import SuppliersList


class SuppliersListViewTestCase(TestCase):
    def setUp(self):
        Suppliers.objects.create(supplier_name='supplier 1',
                               supplier_phone_number='123456789',
                               supplier_email='supplier1@gmail.com',
                               supplier_identification_number='999888777',
                               supplier_accountable_person='Lord Stratton',
                               )
        Suppliers.objects.create(supplier_name='supplier 2',
                               supplier_phone_number='0888888888',
                               supplier_email='strange2@gmail.com',
                               supplier_identification_number='777777777',
                               supplier_accountable_person='John Doe',
                               )
        Suppliers.objects.create(supplier_name='Random Stranger',
                               supplier_email='random@gmail.com',
                               supplier_accountable_person='Random Stranger',
                               )

    def test_get_queryset_with_numbers_for_one_match(self):
        view = SuppliersList()
        request = RequestFactory().get('/suppliers/', {'search_query': '123'})
        view.request = request
        queryset = view.get_queryset()
        self.assertEqual(queryset.count(), 1)
        self.assertEqual(queryset.first().supplier_name, 'supplier 1')

    def test_get_queryset_with_text_for_one_match(self):
        view = SuppliersList()
        request = RequestFactory().get('/suppliers/', {'search_query': 'dom'})
        view.request = request
        queryset = view.get_queryset()
        self.assertEqual(queryset.count(), 1)
        self.assertEqual(queryset.first().supplier_name, 'Random Stranger')

    def test_get_queryset_with_text_for_no_match(self):
        view = SuppliersList()
        request = RequestFactory().get('/suppliers/', {'search_query': 'bru'})
        view.request = request
        queryset = view.get_queryset()
        self.assertEqual(queryset.count(), 0)

    def test_get_queryset_with_text_for_match_all(self):
        view = SuppliersList()
        request = RequestFactory().get('/suppliers/', {'search_query': 'stra'})
        view.request = request
        queryset = view.get_queryset()
        self.assertEqual(queryset.count(), 3)


class suppliersListViewIntegrationTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='password')
        self.client.login(username='testuser', password='password')

        Suppliers.objects.create(supplier_name='supplier 1',
                               supplier_phone_number='123456789',
                               supplier_email='supplier1@gmail.com',
                               supplier_identification_number='999888777',
                               supplier_accountable_person='Lord Stratton',
                               )
        Suppliers.objects.create(supplier_name='supplier 2',
                               supplier_phone_number='0888888888',
                               supplier_email='strange2@gmail.com',
                               supplier_identification_number='777777777',
                               supplier_accountable_person='John Doe',
                               )
        Suppliers.objects.create(supplier_name='Random Stranger',
                               supplier_email='random@gmail.com',
                               supplier_accountable_person='Random Stranger',
                               )

    def test_suppliers_list_view(self):
        response = self.client.get(reverse('suppliers_list'), {'search_query': '123'})
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'supplier 1')
        self.assertNotContains(response, 'supplier 2')
        self.assertNotContains(response, 'Random Stranger')



