from app.models import Transaction
from app import db

class TransactionDao:
    def get_instance(schema, account_id):
        return Transaction(**schema, account_id=account_id)

    def rollback():
        db.session.rollback()
