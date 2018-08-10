from decimal import Decimal, InvalidOperation, ROUND_HALF_UP

from babel.numbers import format_currency

from money.currency import Currency
from money.exceptions import InvalidOperandType, InvalidAmount, ExchangeBackendNotSet, ExchangeRateNotFound
from money.exchange import xrates


class Money:
    """Class representing a monetary amount."""

    _rounding_mode = ROUND_HALF_UP

    def __init__(self, amount, currency):
        if not isinstance(currency, Currency):
            currency = Currency(str(currency))

        try:
            self._amount = Decimal(str(amount))
        except InvalidOperation:
            raise InvalidAmount(amount)

        self._currency = currency

    @property
    def real(self) -> Decimal:
        """Returns the real amount (without rounding)."""

        return self._amount

    @property
    def amount(self) -> Decimal:
        """Returns the amount rounded to the correct number of decimal places for the currency."""

        return self._round()

    @property
    def currency(self) -> Currency:
        """Returns the currency."""

        return self._currency

    def __repr__(self):
        return '{} {}'.format(self._currency, self.amount)

    def __str__(self):
        return self.format()

    def __hash__(self):
        return hash((self._amount, self._currency))

    def __lt__(self, other):
        if not isinstance(other, Money):
            raise InvalidOperandType(other, '<')

        other = other.to(self._currency)

        return self._amount < other.real

    def __le__(self, other):
        if not isinstance(other, Money):
            raise InvalidOperandType(other, '<=')

        other = other.to(self._currency)

        return self._amount <= other.real

    def __eq__(self, other):
        if not isinstance(other, Money):
            return False

        return self.amount == other.amount and self._currency.currency_code == other.currency.currency_code

    def __ne__(self, other):
        return not self == other

    def __ge__(self, other):
        if not isinstance(other, Money):
            raise InvalidOperandType(other, '>=')

        other = other.to(self._currency)

        return self._amount >= other.real

    def __gt__(self, other):
        if not isinstance(other, Money):
            raise InvalidOperandType(other, '>=')

        other = other.to(self._currency)

        return self._amount > other.real

    def __add__(self, other):
        other = self._parse_other(other)

        return self.__class__(self._amount + other, self._currency)

    def __radd__(self, other):
        other = self._parse_other(other)

        return self.__class__(other + self._amount, self._currency)

    def __sub__(self, other):
        other = self._parse_other(other)

        return self.__class__(self._amount - other, self._currency)

    def __rsub__(self, other):
        other = self._parse_other(other)

        return self.__class__(other - self._amount, self._currency)

    def __mul__(self, other):
        other = self._parse_other(other)

        return self.__class__(self._amount * other, self._currency)

    def __rmul__(self, other):
        other = self._parse_other(other)

        return self.__class__(other * self._amount, self._currency)

    def __truediv__(self, other, inverse=False):
        other = self._parse_other(other)

        if other == Decimal(0):
            raise ZeroDivisionError

        return self.__class__(self._amount / other, self._currency)

    def __rtruediv__(self, other):
        other = self._parse_other(other)

        if self._amount == Decimal(0):
            raise ZeroDivisionError

        return self.__class__(other / self._amount, self._currency)

    def __floordiv__(self, other):
        other = self._parse_other(other)

        if other == Decimal(0):
            raise ZeroDivisionError

        return self.__class__(self._amount // other, self._currency)

    def __rfloordiv__(self, other):
        other = self._parse_other(other)

        if self._amount == Decimal(0):
            raise ZeroDivisionError

        return self.__class__(other // self._amount, self._currency)

    def __mod__(self, other):
        other = self._parse_other(other)

        if other == Decimal(0):
            raise ZeroDivisionError

        return self.__class__(self._amount % other, self._currency)

    def __rmod__(self, other):
        other = self._parse_other(other)

        if self._amount == Decimal(0):
            raise ZeroDivisionError

        return self.__class__(other % self._amount, self._currency)

    def __neg__(self):
        return self.__class__(-self._amount, self._currency)

    def __pos__(self):
        return self.__class__(+self._amount, self._currency)

    def __abs__(self):
        return self.__class__(abs(self._amount), self._currency)

    def __int__(self):
        return int(self._amount)

    def __float__(self):
        return float(self._amount)

    def __bool__(self):
        return bool(self._amount)

    def __round__(self, n=0):
        return self.__class__(round(self._amount, n), self._currency)

    def to(self, currency):
        """Returns the equivalent money object in another currency."""

        if currency == self._currency:
            return self

        if xrates.backend is None:
            raise ExchangeBackendNotSet()

        if not isinstance(currency, Currency):
            currency = Currency(currency)

        rate = xrates.backend.quotation(self._currency.currency_code, currency.currency_code)
        if rate is None:
            raise ExchangeRateNotFound(xrates.backend_name, self._currency, currency)

        return self.__class__(self._amount * rate, currency)

    def format(self, locale: str = 'en_US') -> str:
        """Returns a string of the currency formatted for the specified locale."""

        return format_currency(self._amount, self.currency.currency_code, locale=locale)

    def _parse_other(self, other) -> Decimal:
        if isinstance(other, Money):
            return other.to(self._currency).real
        return Decimal(other)

    def _round(self) -> Decimal:
        sub_units = Decimal(str(1 / self._currency.sub_unit).rstrip('0'))
        sub_units_rounded = self._amount.quantize(sub_units, rounding=Money._rounding_mode)

        decimal_precision = Decimal(str(1 / (10 ** self._currency.default_fraction_digits)).rstrip('0'))
        return sub_units_rounded.quantize(decimal_precision, rounding=Money._rounding_mode)

    @classmethod
    def set_rounding_mode(cls, mode):
        cls._rounding_mode = mode
