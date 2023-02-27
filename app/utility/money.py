from decimal import *
getcontext().prec = 2

class Money:
    def __init__(self, amount):
        if not isinstance(amount, str) and not isinstance(amount, Decimal):
            raise ValueError('Invalid amount provided')
        self.amount = Decimal(amount)
        self.currency = 'NGN'

    def add(self, other):
        self.amount += other.amount

    def subtract(self, other):
        self.amount -= other.amount

    def to_amount(self):
        return str(self.amount)

    def is_zero(self):
        return self.amount == 0
