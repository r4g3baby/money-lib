import pytest

from money.currency import Currency
from money.exceptions import UnknownCurrencyCode


def test_construction():
    currency = Currency('USD')

    assert currency.currency_code == 'USD'
    assert currency.display_name == 'US Dollar'
    assert currency.numeric_code == 840
    assert currency.default_fraction_digits == 2
    assert currency.sub_unit == 100

    currency = Currency('jpY')

    assert currency.currency_code == 'JPY'
    assert currency.display_name == 'Yen'
    assert currency.numeric_code == 392
    assert currency.default_fraction_digits == 0
    assert currency.sub_unit == 1

    with pytest.raises(UnknownCurrencyCode):
        Currency('dummy value')


def test_add_currency():
    Currency.add_currency('DUMMY', 'Custom', 143, 4, 30)

    currency = Currency('DUMMY')

    assert currency.currency_code == 'DUMMY'
    assert currency.display_name == 'Custom'
    assert currency.numeric_code == 143
    assert currency.default_fraction_digits == 4
    assert currency.sub_unit == 30


def test_remove_currency():
    del Currency.CURRENCIES['DUMMY']

    with pytest.raises(UnknownCurrencyCode):
        Currency('DUMMY')
