from datetime import datetime
import uuid

from app import db
from app.models import Account
from app.utility import Money

class Transaction(db.Model):
    __tablename__ = 'transactions'

    id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    transaction_id = db.Column(db.String, nullable=False)
    transaction_amount = db.Column(db.Numeric(12, 2), nullable=False)
    transaction_description = db.Column(db.String, nullable=False)
    transaction_type = db.Column(db.String, nullable=False)
    transaction_status = db.Column(db.String, nullable=False)
    transaction_account_id = db.Column(db.Integer, db.ForeignKey('accounts.id'))
    entry_date = db.Column(db.DateTime, default=datetime.utcnow)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    def __init__(self, transaction_amount, transaction_description, transaction_type, account_id):
        self.transaction_id = uuid.uuid4()
        self.transaction_amount = Money(transaction_amount).balance()
        self.transaction_description = transaction_description
        self.transaction_type = transaction_type
        self.account = Account.query.filter_by(id=account_id).first()

    def save(self):
        db.session.add(self)
