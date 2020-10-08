from decimal import Decimal

import pytest

from money import Money, xrates
from money.exceptions import ExchangeBackendNotSet, ExchangeRateNotFound, InvalidExchangeBackend
from money.exchange import SimpleBackend


class TestExchange:
    @staticmethod
    def teardown_method():
        xrates.backend = None

    def test_set_backend_str(self):
        xrates.backend = 'money.exchange.SimpleBackend'

        assert xrates.backend is not None
        assert xrates.backend_name == 'SimpleBackend'

    def test_set_backend_class(self):
        xrates.backend = SimpleBackend

        assert xrates.backend is not None
        assert xrates.backend_name == 'SimpleBackend'

    def test_set_backend_instance(self):
        xrates.backend = SimpleBackend()

        assert xrates.backend is not None
        assert xrates.backend_name == 'SimpleBackend'

    def test_set_invalid_backend(self):
        with pytest.raises(InvalidExchangeBackend):
            xrates.backend = True

    def test_unset_backend(self):
        xrates.backend = 'money.exchange.SimpleBackend'

        assert xrates.backend is not None
        assert xrates.backend_name == 'SimpleBackend'

        xrates.backend = None

        assert xrates.backend is None

    def test_backend_not_set(self):
        with pytest.raises(ExchangeBackendNotSet):
            _ = xrates.backend_name

        with pytest.raises(ExchangeBackendNotSet):
            xrates.base = 'USD'

        with pytest.raises(ExchangeBackendNotSet):
            Money('4', 'USD').to('JPY')


class TestSimpleBackend:
    @classmethod
    def setup_class(cls):
        xrates.backend = 'money.exchange.SimpleBackend'
        xrates.base = 'USD'
        xrates.setrate('EUR', Decimal(2))
        xrates.setrate('JPY', Decimal(8))

    @classmethod
    def teardown_class(cls):
        xrates.backend = None

    def test_base(self):
        assert xrates.base == 'USD'

    def test_rate(self):
        assert xrates.rate('USD') == 1
        assert xrates.rate('EUR') == 2
        assert xrates.rate('JPY') == 8
        assert xrates.rate('AUD') is None

    def test_quotation(self):
        assert xrates.quotation('USD', 'USD') == 1
        assert xrates.quotation('USD', 'EUR') == 2
        assert xrates.quotation('USD', 'JPY') == 8
        assert xrates.quotation('EUR', 'USD') == 0.5
        assert xrates.quotation('EUR', 'EUR') == 1
        assert xrates.quotation('EUR', 'JPY') == 4
        assert xrates.quotation('JPY', 'USD') == 0.125
        assert xrates.quotation('JPY', 'EUR') == 0.25
        assert xrates.quotation('JPY', 'JPY') == 1

    def test_conversion(self):
        money = Money('4', 'USD').to('EUR')

        assert money.amount == 8
        assert money.currency == 'EUR'

        money = Money('4', 'USD').to('JPY')

        assert money.amount == 32
        assert money.currency == 'JPY'

        with pytest.raises(ExchangeRateNotFound):
            Money('4', 'EUR').to('GBP')
