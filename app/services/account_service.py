from app.dao import AccountDao
from app.schemas import account_schema
from app.exceptions import AppException

class AccountService:
    def create_account(payload, subscriber):
        trimmed_payload = { 'account_name': payload['account_name'] }
        user_id = subscriber['id']
        schema = account_schema.load(trimmed_payload)

        if AccountDao.has_account(user_id):
            raise AppException('Cannot create more than one account at this time', 400)

        try:
            account = AccountDao.create_account(schema['account_name'], user_id)
            return account_schema.dump(account)
        except:
            AccountDao.rollback()
            raise AppException('Could not create account', 500)

    def get_account(account_id, subscriber):
        user_id = subscriber['id']
        account = AccountDao.get_account_by(account_id, user_id)
        return account_schema.dump(account)

    def update_account(account_id, payload, subscriber):
        trimmed_payload = { 'account_name': payload['account_name'] }
        schema = account_schema.load(trimmed_payload)
        user_id = subscriber['id']

        if not AccountDao.has_account(user_id):
            raise AppException('Cannot update non-existent account, kindly create one first', 400)

        try:
            account = AccountDao.update_account(account_id, schema['account_name'], user_id)
            return account_schema.dump(account)
        except:
            AccountDao.rollback()
            raise AppException('Could not update account', 500)
