from decimal import Decimal

from django.db import models
from django.utils.translation import gettext_lazy as _

from money import Currency, Money, forms


def _currency_field_name(name): return '{}_currency'.format(name)


class MoneyFieldProxy(object):
    def __init__(self, field):
        self.field = field
        self.currency_name = _currency_field_name(self.field.name)

    def __set__(self, obj, value):
        if isinstance(value, Money):
            obj.__dict__[self.field.name] = value
            setattr(obj, self.currency_name, value.currency)
        else:
            obj.__dict__[self.field.name] = self.field.to_python(value)

    def __get__(self, obj, type=None):
        if obj is None:
            return self

        amount = obj.__dict__[self.field.name]
        if amount is None:
            return None
        else:
            return Money(amount, getattr(obj, self.currency_name))


class CurrencyField(models.CharField):
    description = _("Currency Object")

    def __init__(self, *args, **kwargs):
        default = kwargs.get('default', None)
        if isinstance(default, Currency):
            default = default.code

        kwargs['max_length'] = 3
        kwargs['default'] = default

        super().__init__(*args, **kwargs)


class MoneyField(models.DecimalField):
    description = _("Money Object")

    def __init__(self, verbose_name=None, name=None, max_digits=None, decimal_places=None, default_currency=None,
                 currency_choices=None, **kwargs):
        default = kwargs.get('default', None)
        if not default_currency and default is not None:
            default_currency = default.currency

        self.default_currency = default_currency
        self.currency_choices = currency_choices
        self.nullable = kwargs.get('null', False)

        super().__init__(verbose_name, name, max_digits, decimal_places, **kwargs)

    def contribute_to_class(self, cls, name, private_only=False):
        currency_field = CurrencyField(
            default=self.default_currency, choices=self.currency_choices,
            null=self.nullable, editable=False
        )
        currency_field.creation_counter = self.creation_counter
        cls.add_to_class(_currency_field_name(name), currency_field)

        super().contribute_to_class(cls, name, private_only)

        setattr(cls, self.name, MoneyFieldProxy(self))

    def deconstruct(self):
        name, path, args, kwargs = super().deconstruct()

        if isinstance(self.default, Money):
            kwargs['default'] = Decimal.__str__(self.default)
        if self.default_currency is not None:
            kwargs['default_currency'] = str(self.default_currency)
        if self.currency_choices is not None:
            kwargs['currency_choices'] = self.currency_choices

        return name, path, args, kwargs

    def formfield(self, **kwargs):
        default = self.default
        if isinstance(default, Money):
            default = default.amount

        return super().formfield(**{
            'form_class': forms.MoneyField,
            'default_amount': default,
            'default_currency': self.default_currency,
            'choices': self.currency_choices,
            **kwargs
        })
