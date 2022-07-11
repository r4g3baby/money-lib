class MoneyException(Exception):
    pass


class CurrencyException(MoneyException):
    pass


class InvalidCurrencyFormat(CurrencyException, ValueError):
    def __init__(self, currency):
        msg = (
            f"Currency not in ISO 4217 format: '{currency}'."
        )
        super().__init__(msg)


class ExchangeError(MoneyException):
    pass


class InvalidExchangeBackend(ExchangeError):
    def __init__(self):
        msg = (
            'Parameter \'backend\' isn\'t a subclass of money.exchange.BaseBackend.'
        )
        super().__init__(msg)


class ExchangeBackendNotSet(ExchangeError):
    def __init__(self):
        msg = (
            'Exchange backend hasn\'t been set yet. Set it using '
            'money.xrates.backend = \'path.to.backend\'.'
        )
        super().__init__(msg)


class ExchangeRateNotFound(ExchangeError):
    def __init__(self, backend, origin, target):
        msg = (
            f"Rate not found in backend '{backend}': {origin}/{target}."
        )
        super().__init__(msg)
