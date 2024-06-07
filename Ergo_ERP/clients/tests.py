from django.test import TestCase, RequestFactory
from django.urls import reverse
from django.contrib.auth.models import User
from .models import Clients
from .views import ClientsList


class ClientsListViewTestCase(TestCase):
    def setUp(self):
        Clients.objects.create(client_names='Client 1',
                               client_phone_number='123456789',
                               client_email='client1@gmail.com',
                               client_identification_number='999888777',
                               client_accountable_person='Lord Stratton',
                               client_card_code='777888999'
                               )
        Clients.objects.create(client_names='Client 2',
                               client_phone_number='0888888888',
                               client_email='strange2@gmail.com',
                               client_identification_number='777777777',
                               client_accountable_person='John Doe',
                               client_card_code='999999999'
                               )
        Clients.objects.create(client_names='Random Stranger',
                               client_email='random@gmail.com',
                               client_accountable_person='Random Stranger',
                               )

    def test_get_queryset_with_numbers_for_one_match(self):
        view = ClientsList()
        request = RequestFactory().get('/clients/', {'search_query': '123'})
        view.request = request
        queryset = view.get_queryset()
        self.assertEqual(queryset.count(), 1)
        self.assertEqual(queryset.first().client_names, 'Client 1')

    def test_get_queryset_with_text_for_one_match(self):
        view = ClientsList()
        request = RequestFactory().get('/clients/', {'search_query': 'dom'})
        view.request = request
        queryset = view.get_queryset()
        self.assertEqual(queryset.count(), 1)
        self.assertEqual(queryset.first().client_names, 'Random Stranger')

    def test_get_queryset_with_text_for_no_match(self):
        view = ClientsList()
        request = RequestFactory().get('/clients/', {'search_query': 'bru'})
        view.request = request
        queryset = view.get_queryset()
        self.assertEqual(queryset.count(), 0)

    def test_get_queryset_with_text_for_match_all(self):
        view = ClientsList()
        request = RequestFactory().get('/clients/', {'search_query': 'stra'})
        view.request = request
        queryset = view.get_queryset()
        self.assertEqual(queryset.count(), 3)


class ClientsListViewIntegrationTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='password')
        self.client.login(username='testuser', password='password')

        Clients.objects.create(client_names='Client 1',
                               client_phone_number='123456789',
                               client_email='client1@gmail.com',
                               client_identification_number='999888777',
                               client_accountable_person='Lord Stratton',
                               client_card_code='777888999'
                               )
        Clients.objects.create(client_names='Client 2',
                               client_phone_number='0888888888',
                               client_email='strange2@gmail.com',
                               client_identification_number='777777777',
                               client_accountable_person='John Doe',
                               client_card_code='999999999'
                               )
        Clients.objects.create(client_names='Random Stranger',
                               client_email='random@gmail.com',
                               client_accountable_person='Random Stranger',
                               )

    def test_clients_list_view(self):
        response = self.client.get(reverse('clients_list'), {'search_query': '123'})
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Client 1')
        self.assertNotContains(response, 'Client 2')
        self.assertNotContains(response, 'Random Stranger')



