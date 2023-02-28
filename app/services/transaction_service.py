from flask import current_app
from requests.exceptions import Timeout

from app.schemas import transaction_schema, transactions_schema
from app.dao import AccountDao, TransactionDao
from app.exceptions import AppException
from app.utility import Money, TransactionType, TransactionStatus
from app.services.http_service import HttpService
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
            # IP_URL has rate limiting, but we don't want that to limit us, no pun intended
            ip_response = HttpService.get(current_app.config['IP_URL'], {'format': 'json'})
            transaction.origin_ip = ip_response['ip']
        except Timeout as e:
            current_app.logger.info('Taking too long to fetch ip, skipping without ip', e)
        except Exception as e:
            raise AppException('Failed to fetch origin ip', 500, e)

        try:
            account, transaction = AccountDao.save_transaction(account, transaction)
            db.session.commit()
            return transaction_schema.dump(transaction)
        except Exception as e:
            db.session.rollback()
            raise AppException('Error executing transaction', 500, e)

    def search(account_id, subscriber, offset, limit, description):
        user_id = subscriber['id']

        account = AccountDao.get_account_by(id=account_id, account_holder_id=user_id)
        if not account:
            raise AppException('Account not found', 404)

        filtered_transaction, total = TransactionService.__filter_transaction(account, offset, limit, description)
        return transactions_schema.dump(filtered_transaction), total

    def __filter_transaction(account, offset, limit, description):
        transactions = account.transactions
        if description is None:
            total = len(transactions)
            return transactions[offset:][0:limit], total

        txn_by_desc = [txn for txn in transactions if description.lower() in txn.transaction_description.lower()]
        total = len(txn_by_desc)
        return txn_by_desc[offset:][0:limit], total

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
