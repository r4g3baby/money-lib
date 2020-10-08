from django import forms


class MoneyWidget(forms.MultiWidget):
    def __init__(self, amount_widget=forms.TextInput, currency_widget=forms.Select, choices=None, attrs=None):
        if isinstance(currency_widget, type):
            currency_widget = currency_widget(choices=choices)

        super().__init__((amount_widget, currency_widget), attrs)

    def decompress(self, value):
        if value is not None:
            if isinstance(value, (list, tuple)):
                return value
            return [value.amount, value.currency]
        return None
