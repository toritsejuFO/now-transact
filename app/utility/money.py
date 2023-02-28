from decimal import *
getcontext().prec = 2

class Money:
    def __init__(self, amount):
        if not isinstance(amount, str) and not isinstance(amount, Decimal) and not isinstance(amount, Money):
            raise ValueError('Invalid amount provided')
        if isinstance(amount, Money):
            self.__validate(amount)
            self.amount = amount.amount
            self.currency = amount.currency
        else:
            self.amount = Decimal(amount)
            self.currency = 'NGN'

    def add(self, other):
        self.__validate(other)
        self.amount += other.amount
        return self

    def subtract(self, other):
        self.__validate(other)
        self.amount -= other.amount
        return self

    def balance(self):
        return str(self.amount)

    def is_zero(self):
        return self.amount == 0

    def is_negative(self):
        return self.amount < 0

    def __validate(self, other):
        if self.currency is not other.currency:
            raise ValueError('Cannot operate on money with different currency')
