from unittest import TestCase
from unittest.mock import MagicMock, patch

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


class ProductsListSaveToDocumentTest(TestCase):
    def setUp(self):
        self.document_instance = MagicMock()
        self.document_instance.id = 1

    def test_document_no_department(self):
        form1 = MagicMock()
        form1.cleaned_data = {'name': 'Bucket', 'quantity': 1, 'sales_document': ''}
        form1.save.return_value = form1

        form2 = MagicMock()
        form2.cleaned_data = {'name': 'Socket', 'quantity': 2, 'sales_document': ''}
        form2.save.return_value = form2

        formset = [form1, form2]

        with patch('Ergo_ERP.common.helper_functions.DatabaseError', Exception):
            saved_product_instances = products_list_save_to_document(formset, self.document_instance, 'sales_document')

        self.assertEqual(len(saved_product_instances), 2)
        self.assertEqual(saved_product_instances[0].cleaned_data['name'], 'Bucket')
        self.assertEqual(saved_product_instances[0].cleaned_data['quantity'], 1)
        self.assertEqual(saved_product_instances[1].cleaned_data['name'], 'Socket')
        self.assertEqual(saved_product_instances[1].cleaned_data['quantity'], 2)

        form1.save.assert_called_once()
        form2.save.assert_called_once()
