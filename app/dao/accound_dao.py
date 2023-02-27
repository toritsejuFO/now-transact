from app.models import Account
from app import db

class AccountDao:
    def create_account(account_name, account_holder_id):
        account = Account(account_name, account_holder_id)
        account.save()
        return account

    def has_account(account_holder_id):
        count = Account.query.filter_by(account_holder_id=account_holder_id).count()
        return count > 0

    def rollback():
        db.session.rollback()
