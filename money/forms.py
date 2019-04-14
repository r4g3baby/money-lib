from django import forms

from money import Money
from money.widgets import MoneyWidget


class MoneyField(forms.MultiValueField):
    def __init__(self, amount_widget=None, default_amount=None, max_value=None, min_value=None, max_digits=None,
                 decimal_places=None, currency_widget=None, default_currency=None, choices=(), *args, **kwargs):
        amount_field = forms.DecimalField(
            widget=amount_widget or forms.DecimalField.widget,
            max_value=max_value, min_value=min_value, max_digits=max_digits, decimal_places=decimal_places
        )
        currency_field = forms.ChoiceField(
            widget=currency_widget or forms.ChoiceField.widget,
            choices=choices
        )

        self.widget = MoneyWidget(
            amount_widget=amount_field.widget,
            currency_widget=currency_field.widget,
            choices=choices
        )

        super().__init__((amount_field, currency_field), *args, **kwargs)

        self.initial = [default_amount, default_currency]

    def compress(self, data_list):
        if data_list:
            if not self.required and (data_list[0] in self.empty_values or data_list[1] in self.empty_values):
                return None
            return Money(*data_list[:2])
        return None
