from app.models import Transaction

class TransactionDao:
    def get_instance(schema, account_id):
        return Transaction(**schema, account_id=account_id)
