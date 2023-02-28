from datetime import datetime

from app import db
from app.models import User

class Account(db.Model):
    __tablename__ = 'accounts'

    id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    account_name = db.Column(db.String, nullable=False)
    account_balance = db.Column(db.Numeric(12, 2), nullable=False)
    account_number = db.Column(db.BigInteger, nullable=False)
    account_type = db.Column(db.String, nullable=False)
    account_holder_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    transactions = db.relationship('Transaction', backref='account', order_by='desc(Transaction.created_at)')
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    def __init__(self, account_name, account_balance, account_number, account_type, account_holder_id):
        self.account_name = account_name
        self.account_balance = account_balance
        self.account_number = account_number
        self.account_type = account_type
        self.account_holder = User.query.filter_by(id=account_holder_id).first()

    def save(self):
        db.session.add(self)
