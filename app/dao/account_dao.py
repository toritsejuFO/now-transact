from app.models import Account
from app import db

class AccountDao:
    def create_account(user_id, schema):
        account = Account(**schema, account_holder_id=user_id)
        account.save()
        return account

    def get_account_by(**kwargs):
        account = Account.query.filter_by(**kwargs).first()
        return account

    def update_account(account_id, account_name, user_id):
        account = AccountDao.get_account_by(id=account_id, account_holder_id=user_id)
        account.account_name = account_name
        account.save()
        return account

    def delete_account(account):
        db.session.delete(account)

    def save_transaction(account, transaction):
        account.transactions.append(transaction)
        account.save()
        return account, transaction

    def has_account(user_id):
        count = Account.query.filter_by(account_holder_id=user_id).count()
        return count > 0

    def exist_by(**kwargs):
        count = Account.query.filter_by(**kwargs).count()
        return count > 0
