from decimal import Decimal, InvalidOperation

import pytest

from money import Money, xrates
from money.exceptions import InvalidCurrencyFormat


def setup_module():
    xrates.backend = 'money.exchange.SimpleBackend'
    xrates.base = 'USD'
    xrates.setrate('EUR', Decimal(2))


def teardown_module():
    xrates.backend = None


def test_construction():
    money = Money('3.95', 'USD')

    assert money == Decimal('3.95')
    assert money.amount == Decimal('3.95')
    assert money.currency == 'USD'

    money = Money(4.56, 'GBP')

    assert money == Decimal(4.56)
    assert money.amount == Decimal('4.56')
    assert money.currency == 'GBP'

    money = Money(4, 'AUD')

    assert money == Decimal('4')
    assert money.amount == Decimal('4')
    assert money.currency == 'AUD'

    with pytest.raises(InvalidCurrencyFormat):
        Money(1, 'dummy value')

    with pytest.raises(InvalidOperation):
        Money('dummy value', 'USD')


def test_format():
    assert Money(5.364, 'USD').format() == '$5.36'
    assert Money(7.452, 'JPY').format() == '¥7'
    assert Money(9.345, 'JPY').format('ja_JP') == '￥9'


def test_str():
    assert str(Money(8, 'USD')) == '$8.00'
    assert str(Money(8, 'JPY')) == '¥8'


def test_lt():
    assert Money(8, 'USD') < Money(10, 'USD')
    assert not Money(10, 'USD') < Money(8, 'USD')

    assert Money(8, 'USD') < Money(20, 'EUR')
    assert not Money(8, 'USD') < Money(10, 'EUR')


def test_le():
    assert Money(8, 'USD') <= Money(8, 'USD')
    assert not Money(8, 'USD') <= Money(6, 'USD')

    assert Money(8, 'USD') <= Money(16, 'EUR')
    assert not Money(8, 'USD') <= Money(10, 'EUR')


def test_eq():
    assert Money(8, 'USD') == Money(8, 'USD')
    assert not Money(8, 'USD') == Money(10, 'USD')


def test_ne():
    assert Money(8, 'USD') != Money(8, 'EUR')
    assert Money(8, 'USD') != Money(10, 'USD')


def test_ge():
    assert Money(8, 'USD') >= Money(8, 'USD')
    assert not Money(6, 'USD') >= Money(8, 'USD')

    assert Money(8, 'USD') >= Money(16, 'EUR')
    assert not Money(8, 'USD') >= Money(20, 'EUR')


def test_gt():
    assert Money(10, 'USD') > Money(8, 'USD')
    assert not Money(8, 'USD') > Money(10, 'USD')

    assert Money(8, 'USD') > Money(10, 'EUR')
    assert not Money(8, 'USD') > Money(20, 'EUR')


def test_add():
    assert Money(4, 'USD') + Money(4, 'USD') == Money(8, 'USD')
    assert Money(4, 'USD') + Money(2, 'EUR') == Money(5, 'USD')
    assert Money(4, 'USD') + 4 == Money(8, 'USD')


def test_sub():
    assert Money(4, 'USD') - Money(4, 'USD') == Money(0, 'USD')
    assert Money(4, 'USD') - Money(2, 'EUR') == Money(3, 'USD')
    assert Money(4, 'USD') - 4 == Money(0, 'USD')


def test_mul():
    assert Money(4, 'USD') * Money(4, 'USD') == Money(16, 'USD')
    assert Money(4, 'USD') * Money(2, 'EUR') == Money(4, 'USD')
    assert Money(4, 'USD') * 4 == Money(16, 'USD')


def test_truediv():
    assert Money(4, 'USD') / Money(4, 'USD') == Money(1, 'USD')
    assert Money(4, 'USD') / Money(2, 'EUR') == Money(4, 'USD')
    assert Money(4, 'USD') / 4 == Money(1, 'USD')

    with pytest.raises(ZeroDivisionError):
        assert Money(4, 'USD') / Money(0, 'USD')
        assert Money(4, 'USD') / 0


def test_floordiv():
    assert Money(4, 'USD') // Money(4, 'USD') == Money(1, 'USD')
    assert Money(4, 'USD') // Money(2, 'EUR') == Money(4, 'USD')
    assert Money(4, 'USD') // 4 == Money(1, 'USD')

    with pytest.raises(ZeroDivisionError):
        assert Money(4, 'USD') // Money(0, 'USD')
        assert Money(4, 'USD') // 0


def test_mod():
    assert Money(4, 'USD') % Money(4, 'USD') == Money(0, 'USD')
    assert Money(4, 'USD') % Money(2, 'EUR') == Money(0, 'USD')
    assert Money(4, 'USD') % 4 == Money(0, 'USD')

    with pytest.raises(InvalidOperation):
        assert Money(4, 'USD') % Money(0, 'USD')
        assert Money(4, 'USD') % 0


def test_neg():
    assert -Money(4, 'USD') == Money(-4, 'USD')
    assert -Money(-4, 'USD') == Money(4, 'USD')


def test_pos():
    assert +Money(4, 'USD') == Money(4, 'USD')
    assert +Money(-4, 'USD') == Money(-4, 'USD')


def test_abs():
    assert abs(Money(4, 'USD')) == Money(4, 'USD')
    assert abs(Money(-4, 'USD')) == Money(4, 'USD')


def test_int():
    assert int(Money(4, 'USD')) == 4
    assert int(Money(4.435, 'EUR')) == 4


def test_float():
    assert float(Money(4, 'USD')) == 4
    assert float(Money(4.435, 'EUR')) == 4.435


def test_bool():
    assert bool(Money(4, 'USD')) is True
    assert bool(Money(0, 'USD')) is False


def test_round():
    assert round(Money(4, 'USD')) == Money(4, 'USD')
    assert round(Money(4, 'EUR')) == Money(4, 'EUR')
    assert round(Money(4.435, 'USD'), 0) == Money(4.0, 'USD')
    assert round(Money(4.435, 'USD'), 1) == Money('4.4', 'USD')
