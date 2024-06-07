from django.test import TestCase, RequestFactory
from django.urls import reverse
from django.contrib.auth.models import User
from .models import ProductsModel
from .views import ProductsList


class ProductsListViewTestCase(TestCase):
    def setUp(self):
        ProductsModel.objects.create(product_name='Bucket',
                                     product_manufacturer='Vertex',
                                     product_type='product',
                                     product_unit='pieces',
                                     product_has_exp_date=False,
                                     product_vat=20,
                                     product_retail_price=10,
                                     product_wholesale_price=9,
                                     product_employee_price=8
                                     )
        ProductsModel.objects.create(product_name='Mop',
                                     product_manufacturer='Vertex',
                                     product_type='product',
                                     product_unit='pieces',
                                     product_has_exp_date=False,
                                     product_vat=20,
                                     product_retail_price=10,
                                     product_wholesale_price=9,
                                     product_employee_price=8
                                     )
        ProductsModel.objects.create(product_name='Socket',
                                     product_manufacturer='Vertex',
                                     product_type='product',
                                     product_unit='pieces',
                                     product_has_exp_date=False,
                                     product_vat=20,
                                     product_retail_price=10,
                                     product_wholesale_price=9,
                                     product_employee_price=8
                                     )

    def test_get_queryset_for_one_match(self):
        view = ProductsList()
        request = RequestFactory().get('/products/', {'search_query': 'op'})
        view.request = request
        queryset = view.get_queryset()
        self.assertEqual(queryset.count(), 1)
        self.assertEqual(queryset.first().product_name, 'Mop')

    def test_get_queryset_for_two_matches(self):
        view = ProductsList()
        request = RequestFactory().get('/products/', {'search_query': 'ket'})
        view.request = request
        queryset = view.get_queryset()
        self.assertEqual(queryset.count(), 2)

    def test_get_queryset_for_no_matches(self):
        view = ProductsList()
        request = RequestFactory().get('/products/', {'search_query': 'Sponge'})
        view.request = request
        queryset = view.get_queryset()
        self.assertEqual(queryset.count(), 0)


class ClientsListViewIntegrationTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='password')
        self.client.login(username='testuser', password='password')

        ProductsModel.objects.create(product_name='Bucket',
                                     product_manufacturer='Vertex',
                                     product_type='product',
                                     product_unit='pieces',
                                     product_has_exp_date=False,
                                     product_vat=20,
                                     product_retail_price=10,
                                     product_wholesale_price=9,
                                     product_employee_price=8
                                     )
        ProductsModel.objects.create(product_name='Mop',
                                     product_manufacturer='Vertex',
                                     product_type='product',
                                     product_unit='pieces',
                                     product_has_exp_date=False,
                                     product_vat=20,
                                     product_retail_price=10,
                                     product_wholesale_price=9,
                                     product_employee_price=8
                                     )
        ProductsModel.objects.create(product_name='Socket',
                                     product_manufacturer='Vertex',
                                     product_type='product',
                                     product_unit='pieces',
                                     product_has_exp_date=False,
                                     product_vat=20,
                                     product_retail_price=10,
                                     product_wholesale_price=9,
                                     product_employee_price=8
                                     )

    def test_products_list_view(self):
        response = self.client.get(reverse('products_list'), {'search_query': 'Buc'})
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Bucket')
        self.assertNotContains(response, 'Mop')
        self.assertNotContains(response, 'Socket')




