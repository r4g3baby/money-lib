import pytest

from money.currency import Currency
from money.exceptions import InvalidCurrencyFormat


def test_construction():
    currency = Currency('USD')

    assert currency.currency_code == 'USD'
    assert currency.precision == 2
    assert currency.display_name() == 'US Dollar'
    assert currency.symbol() == '$'

    currency = Currency('JPY')

    assert currency.currency_code == 'JPY'
    assert currency.precision == 0
    assert currency.display_name() == 'Japanese Yen'
    assert currency.symbol() == '¥'

    with pytest.raises(InvalidCurrencyFormat):
        Currency('dummy value')


def test_locale():
    currency = Currency('USD')

    assert currency.display_name() == 'US Dollar'
    assert currency.display_name('pt_PT') == 'dólar dos Estados Unidos'
    assert currency.display_name('de_DE') == 'US-Dollar'

    assert currency.symbol() == '$'
    assert currency.symbol('pt_PT') == 'US$'
    assert currency.symbol('de_DE') == '$'
