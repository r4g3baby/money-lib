import re

from babel.numbers import get_currency_name, get_currency_precision, get_currency_symbol

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

    def __init__(self, currency_code):
        if not CURRENCY_REGEX.match(currency_code):
            raise InvalidCurrencyFormat(currency_code)

        self._code = currency_code

    @property
    def code(self):
        """Returns the ISO 4217 code of this currency."""

        return self._code

    @property
    def precision(self):
        """Returns the precision of this currency."""

        return get_currency_precision(self._code)

    def display_name(self, locale='en_US'):
        """Returns the name used by the locale for this currency."""

        return get_currency_name(self._code, locale=locale)

    def symbol(self, locale='en_US'):
        """Returns the symbol used by the locale for this currency."""

        return get_currency_symbol(self._code, locale=locale)

    def __repr__(self):
        return 'Currency(\'{}\')'.format(self._code)

    def __str__(self):
        return self._code

    def __reduce__(self):
        return self.__class__, (self._code,)

    def __eq__(self, other):
        if isinstance(other, Currency):
            return other.code == self._code
        if isinstance(other, str):
            return other == self._code
        return NotImplemented

    def __ne__(self, other):
        return not self == other
