import re

from babel.numbers import get_currency_precision, get_currency_name, get_currency_symbol

from money.exceptions import InvalidCurrencyFormat

CURRENCY_REGEX = re.compile('^[A-Z]{3}$')


class Currency:
    """
    Represents a currency identified by its ISO 4217 code.

    Parameters
    ----------
    currency_code: str
        The ISO 4217 code of the currency

    Raises
    ------
    InvalidCurrencyFormat
        If the given currency_code isn't a valid ISO 4217 format
    """

    def __init__(self, currency_code: str):
        if not CURRENCY_REGEX.match(currency_code):
            raise InvalidCurrencyFormat(currency_code)

        self._currency_code = currency_code

    @property
    def currency_code(self) -> str:
        """Returns the ISO 4217 code of this currency."""

        return self._currency_code

    @property
    def precision(self) -> int:
        """Returns the precision of this currency."""

        return get_currency_precision(self._currency_code)

    def display_name(self, locale: str = 'en_US') -> str:
        """Returns the name used by the locale for this currency."""

        return get_currency_name(self._currency_code, locale=locale)

    def symbol(self, locale: str = 'en_US') -> str:
        """Returns the symbol used by the locale for this currency."""

        return get_currency_symbol(self._currency_code, locale=locale)

    def __repr__(self):
        return self._currency_code

    def __str__(self):
        return self._currency_code

    def __eq__(self, other):
        if isinstance(other, Currency):
            return other.currency_code == self._currency_code
        if isinstance(other, str):
            return other == self._currency_code
        return NotImplemented

    def __ne__(self, other):
        return not self == other
