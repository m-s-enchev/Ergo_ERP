from unittest import TestCase
from unittest.mock import MagicMock

from django import forms
from django.forms import formset_factory

from Ergo_ERP.common.helper_functions import is_formset_nonempty, products_list_save_to_document


# -------------------- TEST Helper Functions-----------------------

class TestForm(forms.Form):
    field = forms.CharField(required=False)


class IsFormsetNonemptyTest(TestCase):
    def setUp(self):
        self.TestFormSet = formset_factory(TestForm, extra=1)

    def test_empty_formset(self):
        formset = self.TestFormSet(data={'form-TOTAL_FORMS': '3', 'form-INITIAL_FORMS': '0'})
        formset.is_valid()
        self.assertFalse(is_formset_nonempty(formset))

    def test_formset_with_one_empty_form(self):
        formset = self.TestFormSet(data={
            'form-TOTAL_FORMS': '1',
            'form-INITIAL_FORMS': '0',
            'form-0-field': '',
        })
        formset.is_valid()
        self.assertFalse(is_formset_nonempty(formset))

    def test_formset_with_one_nonempty_form(self):
        formset = self.TestFormSet(data={
            'form-TOTAL_FORMS': '3',
            'form-INITIAL_FORMS': '0',
            'form-0-field': 'Some value',
            'form-1-field': '',
            'form-2-field': '',
        })
        formset.is_valid()
        self.assertTrue(is_formset_nonempty(formset))

    def test_formset_with_multiple_empty_forms(self):
        formset = self.TestFormSet(data={
            'form-TOTAL_FORMS': '3',
            'form-INITIAL_FORMS': '0',
            'form-0-field': '',
            'form-1-field': '',
            'form-2-field': '',
        })
        formset.is_valid()
        self.assertFalse(is_formset_nonempty(formset))


class ProductsListSaveToDocumentTest (TestCase):
    def setUp(self):
        self.TestFormSet = formset_factory(TestForm, extra=1)
        self.name_of_foreignkey_field = 'sales_document'
        self.document_instance = MagicMock()
        self.document_instance.configure_mock(id=1, date='2024-05-05')

    def test_document_no_department(self):
        formset = self.TestFormSet(data={
            'form-TOTAL_FORMS': '2',
            'form-INITIAL_FORMS': '0',
            'form-0-name': 'Bucket',
            'form-0-quantity': '1',
            'form-0-sales_document': '',
            'form-1-name': 'Socket',
            'form-1-quantity': '2',
            'form-1-sales_document': '',

        })
        formset.is_valid()
        saved_product_instances = products_list_save_to_document(formset, self.document_instance, self.name_of_foreignkey_field)
        self.assertEqual(len(saved_product_instances), 1)
