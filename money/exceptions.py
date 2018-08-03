class MoneyException(Exception):
    pass


class InvalidOperandType(MoneyException, TypeError):
    def __init__(self, operand, operation):
        msg = (
            'Unsupported operation between Money and \'{}\': \'{}\'. This '
            'operation can only be performed with another Money object.'
        ).format(type(operand), operation)
        super().__init__(msg)
