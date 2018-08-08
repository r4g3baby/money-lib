class MoneyException(Exception):
    pass


class UnknownCurrencyCode(MoneyException, ValueError):
    def __init__(self, currency):
        msg = (
            'Unknown currency code \'{}\'.'
        ).format(currency)
        super().__init__(msg)


class InvalidAmount(MoneyException, ValueError):
    def __init__(self, amount):
        msg = (
            'Parameter \'amount\' could not be converted to Decimal(): \'{}\'.'
        ).format(amount)
        super().__init__(msg)


class InvalidOperandType(MoneyException, TypeError):
    def __init__(self, operand, operation):
        msg = (
            'Unsupported operation between Money and \'{}\': \'{}\'. This '
            'operation can only be performed with another Money object.'
        ).format(type(operand), operation)
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
            'Rate not found in backend \'{}\': {}/{}.'
        ).format(backend, origin, target)
        super().__init__(msg)
