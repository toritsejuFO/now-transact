import random

from app.dao import AccountDao
from app.schemas import account_schema
from app.exceptions import AppException
from app.utility import Money, AccountType
from app import db

class AccountService:
    def create_account(payload, subscriber):
        trimmed_payload = {
            'account_name': payload['account_name'],
            'account_balance': Money('0.00').balance(),
            'account_number': AccountService.__generate_account_number(),
            'account_type': AccountType.SAVINGS
        }
        user_id = subscriber['id']
        schema = account_schema.load(trimmed_payload)

        if AccountDao.has_account(user_id):
            raise AppException('Cannot create more than one account at this time', 400)

        try:
            account = AccountDao.create_account(user_id, schema)
            db.session.commit()
            return account_schema.dump(account)
        except:
            db.session.rollback()
            raise AppException('Could not create account', 500)

    def get_account(account_id, subscriber):
        user_id = subscriber['id']
        account = AccountDao.get_account_by(id=account_id, account_holder_id=user_id)

        if not account:
            raise AppException('Cannot retrieve non-existent account, kindly create one', 404)

        return account_schema.dump(account)

    def update_account(account_id, payload, subscriber):
        trimmed_payload = { 'account_name': payload['account_name'] }
        schema = account_schema.load(trimmed_payload)
        user_id = subscriber['id']

        if not AccountDao.has_account(user_id):
            raise AppException('Cannot update non-existent account, kindly create one', 400)

        try:
            account = AccountDao.update_account(account_id, schema['account_name'], user_id)
            db.session.commit()
            return account_schema.dump(account)
        except:
            db.session.rollback()
            raise AppException('Could not update account', 500)

    def delete_account(account_id, subscriber):
        user_id = subscriber['id']
        to_delete = AccountDao.get_account_by(id=account_id, account_holder_id=user_id)

        if not to_delete:
            raise AppException('Cannot delete non-existent account, kindly create one', 404)

        if not Money(to_delete.account_balance).is_zero():
            raise AppException('Cannot delete account with non-zero balance, kindly withdraw', 404)

        try:
            AccountDao.delete_account(to_delete)
            db.session.commit()
            return account_schema.dump(to_delete)
        except Exception as e:
            db.session.rollback()
            raise AppException('Could not delete account', 500, e)

    def __generate_account_number():
        number = AccountService.__get_account_number()
        while AccountDao.exist_by(account_number=number):
            number = AccountService.__get_account_number()
        return number

    def __get_account_number():
        return int(''.join([str(random.randint(0, 9)) for _ in range(10)]))
 