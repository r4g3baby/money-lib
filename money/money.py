from decimal import Decimal, ROUND_HALF_UP

from babel.numbers import format_currency

from money import Currency, xrates
from money.exceptions import ExchangeBackendNotSet, ExchangeRateNotFound


def _make_comparison_operator(name):
    method = getattr(Decimal, name, None)

    def operator_func(self, other, *args):
        if isinstance(other, Money):
            other = other.to(self._currency)

        return method(self, other, *args)

    return operator_func


def _make_arithmetic_operator(name):
    method = getattr(Decimal, name, None)

    def operator_func(self, other, *args):
        if isinstance(other, Money):
            other = other.to(self._currency)

        result = method(self, other, *args)
        if result is NotImplemented:
            return NotImplemented

        return self.__class__(result, self._currency)

    return operator_func


def _make_class_operator(name):
    method = getattr(Decimal, name, None)

    def operator_func(self, *args):
        return self.__class__(method(self, *args), self._currency)

    return operator_func


class Money(Decimal):
    """Class representing a monetary amount."""

    _rounding_mode = ROUND_HALF_UP

    __slots__ = ('_currency',)

    def __new__(cls, amount, currency):
        self = super().__new__(cls, amount)

        if not isinstance(currency, Currency):
            currency = Currency(str(currency))

        self._currency = currency

        return self

    @property
    def amount(self):
        """Returns the amount rounded to the correct number of decimal places for the currency."""

        decimal_precision = Decimal(str(1 / (10 ** self._currency.precision)).rstrip('0'))
        return self.quantize(decimal_precision, rounding=Money._rounding_mode)

    @property
    def currency(self):
        """Returns the currency."""

        return self._currency

    def __composite_values__(self):
        # https://docs.sqlalchemy.org/en/14/orm/composites.html
        return Decimal(self), str(self._currency)

    def __repr__(self):
        return f"Money({super().__repr__()}, {self._currency!r})"

    def __str__(self):
        return self.format()

    def __reduce__(self):
        return self.__class__, (Decimal.__str__(self), self._currency)

    def __eq__(self, other):
        result = super().__eq__(other)
        if result is NotImplemented:
            return NotImplemented

        if isinstance(other, Money):
            return result and other._currency == self._currency
        return result

    def __ne__(self, other):
        return not self == other

    def __hash__(self):
        return hash((Decimal(self), self._currency.code))

    __lt__ = _make_comparison_operator('__lt__')
    __le__ = _make_comparison_operator('__le__')
    __gt__ = _make_comparison_operator('__gt__')
    __ge__ = _make_comparison_operator('__ge__')

    __add__ = _make_arithmetic_operator('__add__')
    __radd__ = _make_arithmetic_operator('__radd__')
    __sub__ = _make_arithmetic_operator('__sub__')
    __rsub__ = _make_arithmetic_operator('__rsub__')
    __mul__ = _make_arithmetic_operator('__mul__')
    __rmul__ = _make_arithmetic_operator('__rmul__')
    __truediv__ = _make_arithmetic_operator('__truediv__')
    __rtruediv__ = _make_arithmetic_operator('__rtruediv__')
    __divmod__ = _make_arithmetic_operator('__divmod__')
    __rdivmod__ = _make_arithmetic_operator('__rdivmod__')
    __mod__ = _make_arithmetic_operator('__mod__')
    __rmod__ = _make_arithmetic_operator('__rmod__')
    __floordiv__ = _make_arithmetic_operator('__floordiv__')
    __rfloordiv__ = _make_arithmetic_operator('__rfloordiv__')
    __pow__ = _make_arithmetic_operator('__pow__')
    __rpow__ = _make_arithmetic_operator('__rpow__')

    __neg__ = _make_class_operator('__neg__')
    __pos__ = _make_class_operator('__pos__')
    __abs__ = _make_class_operator('__abs__')
    __round__ = _make_class_operator('__round__')
    __floor__ = _make_class_operator('__floor__')
    __ceil__ = _make_class_operator('__ceil__')

    def to(self, currency):
        """Returns the equivalent money object in another currency."""

        if currency == self._currency:
            return self

        if xrates.backend is None:
            raise ExchangeBackendNotSet()

        if not isinstance(currency, Currency):
            currency = Currency(str(currency))

        rate = xrates.backend.quotation(self._currency.code, currency.code)
        if rate is None:
            raise ExchangeRateNotFound(xrates.backend_name, self._currency, currency)

        return self.__class__(self * rate, currency)

    def format(self, locale='en_US'):
        """Returns a string of the currency formatted for the specified locale."""

        return format_currency(self, self.currency.code, locale=locale).replace('\xa0', ' ')

    @classmethod
    def set_rounding_mode(cls, mode):
        cls._rounding_mode = mode
