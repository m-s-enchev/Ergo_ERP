from decimal import Decimal, ROUND_HALF_UP, InvalidOperation

from django.core.exceptions import ValidationError
from django.forms import forms
from django.utils.translation import gettext_lazy as _


class DecimalFieldsValidationMixin:
    decimal_fields = []

    def clean(self):
        cleaned_data = super().clean()
        for field_name in self.decimal_fields:
            value = cleaned_data.get(field_name)
            if value is not None:
                try:
                    decimal_value = Decimal(value).quantize(Decimal('0.01'), rounding=ROUND_HALF_UP)
                    cleaned_data[field_name] = decimal_value
                except (ValueError, InvalidOperation):
                    raise ValidationError({field_name: _('Invalid number format.')})

                # Example validation: check if value is negative
                if decimal_value < 0:
                    self.add_error(field_name, _('Invalid value - must not be negative.'))

        return cleaned_data
