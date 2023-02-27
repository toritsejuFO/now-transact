from app.dao import AccountDao
from app.schemas import account_schema
from app.exceptions import AppException

class AccountService:
    def create_account(payload, subscriber):
        constrained_payload = { 'account_name': payload['account_name'] }
        user_id = subscriber['id']
        schema = account_schema.load(constrained_payload)

        if AccountDao.has_account(user_id):
            raise AppException('Cannot create more than one account at this time', 400)

        try:
            account = AccountDao.create_account(schema['account_name'], user_id)
            return account_schema.dump(account)
        except:
            AccountDao.rollback()
            raise AppException('Could not create account', 500)
