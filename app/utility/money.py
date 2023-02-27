from decimal import *
getcontext().prec = 2

class Money:
    def __init__(self, amount: str):
        if not isinstance(amount, str):
            raise ValueError('Invalid amount provided, amount must be a string')
        self.amount = Decimal(amount)
        self.currency = 'NGN'

    def add(self, other):
        self.amount += other.amount

    def subtract(self, other):
        self.amount -= other.amount

    def to_amount(self):
        return str(self.amount)
