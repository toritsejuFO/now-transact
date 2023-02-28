from app.schemas import transaction_schema
from app.dao import AccountDao, TransactionDao
from app.exceptions import AppException
from app.utility import Money, TransactionType, TransactionStatus
from app import db

class TransactionService:
    def execute(account_id, payload, subscriber):
        schema = transaction_schema.load(payload)
        user_id = subscriber['id']

        account = AccountDao.get_account_by(id=account_id, account_holder_id=user_id)
        if not account:
            raise AppException('Account not found', 404)

        transaction = TransactionDao.get_instance(schema, account.id)
        TransactionService.__execute(account, transaction)

        try:
            account, transaction = AccountDao.save_transaction(account, transaction)
            db.session.commit()
            return transaction_schema.dump(transaction)
        except Exception as e:
            db.session.rollback()
            raise AppException('Error executing transaction', 500, e)

    def __execute(account, transaction):
        account_money = Money(account.account_balance)
        transaction_money = Money(transaction.transaction_amount)

        if TransactionService.is_debit(transaction.transaction_type):
            if account_money.subtract(transaction_money).is_negative():
                raise AppException('Terminal account balance can not be negative', 400)
            account.account_balance = Money(account.account_balance).subtract(Money(transaction.transaction_amount)).balance()
        elif TransactionService.is_credit(transaction.transaction_type):
            account.account_balance = Money(account.account_balance).add(Money(transaction.transaction_amount)).balance()

        transaction.transaction_status = TransactionStatus.SUCCESS

    def is_debit(transaction_type):
        if transaction_type == TransactionType.WITHDRAWAL:
            return True
        return False

    def is_credit(transaction_type):
        if transaction_type == TransactionType.DEPOSIT:
            return True
        return False
