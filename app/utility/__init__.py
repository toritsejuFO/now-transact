from app.utility.response import Response
from app.utility.money import Money

class AccountType:
    SAVINGS = 'SAVINGS'

class TransactionType:
    DEPOSIT = 'DEPOSIT'
    WITHDRAWAL = 'WITHDRAWAL'
    TRANSFER = 'TRANSFER'

class TransactionStatus:
    PENDING = 'PENDING'
    FAILED = 'FAILED'
    SUCCESS = 'SUCCESS'
