from app.models import Account
from app import db

class AccountDao:
    def create_account(account_name, account_holder_id):
        account = Account(account_name, account_holder_id)
        account.save()
        return account

    def get_account_by(account_id, account_holder_id):
        account = Account.query.filter_by(id=account_id, account_holder_id=account_holder_id).first()
        return account

    def update_account(account_id, account_name, account_holder_id):
        account = AccountDao.get_account_by(account_id, account_holder_id)
        account.account_name = account_name
        account.save()
        return account

    def delete_account(account):
        db.session.delete(account)
        db.session.commit()

    def has_account(account_holder_id):
        count = Account.query.filter_by(account_holder_id=account_holder_id).count()
        return count > 0

    def rollback():
        db.session.rollback()
