from decimal import Decimal

from money.exchange import xrates, SimpleBackend
from money.money import Money


class TestExchange:
    # noinspection PyMethodMayBeStatic
    def setup_method(self):
        xrates.backend = None

    def test_set_backend_str(self):
        assert xrates.backend is None

        xrates.backend = 'money.exchange.SimpleBackend'

        assert xrates.backend is not None
        assert xrates.backend_name == 'SimpleBackend'

    def test_set_backend_class(self):
        assert xrates.backend is None

        xrates.backend = SimpleBackend

        assert xrates.backend is not None
        assert xrates.backend_name == 'SimpleBackend'

    def test_set_backend_instance(self):
        assert xrates.backend is None

        xrates.backend = SimpleBackend()

        assert xrates.backend is not None
        assert xrates.backend_name == 'SimpleBackend'

    def test_unset_backend(self):
        xrates.backend = 'money.exchange.SimpleBackend'

        assert xrates.backend is not None
        assert xrates.backend_name == 'SimpleBackend'

        xrates.backend = None

        assert xrates.backend is None
        assert xrates.backend_name == 'NoneType'


class TestSimpleBackend:
    # noinspection PyMethodMayBeStatic
    def setup_method(self):
        xrates.backend = 'money.exchange.SimpleBackend'
        xrates.base = 'USD'
        xrates.set_rate('EUR', 2)
        xrates.set_rate('JPY', 8)

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
        money = Money(4, 'USD').to('EUR')

        assert money.real == Decimal(8)
        assert money.amount == Decimal(8)
        assert money.currency.currency_code == 'EUR'

        money = Money(4, 'USD').to('JPY')

        assert money.real == Decimal(32)
        assert money.amount == Decimal(32)
        assert money.currency.currency_code == 'JPY'
