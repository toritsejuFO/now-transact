from datetime import datetime
import random

from app import db
from app.models import User
from app.utility import Money

class Account(db.Model):
    __tablename__ = 'accounts'

    id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    account_name = db.Column(db.String, nullable=False)
    account_balance = db.Column(db.Numeric(12, 2), nullable=False)
    account_number = db.Column(db.BigInteger, nullable=False)
    account_type = db.Column(db.String, nullable=False)
    account_holder_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    def __init__(self, account_name, account_holder_id):
        self.account_name = account_name
        self.account_balance = Money('0.00').to_amount()
        self.account_number = Account.__generate_account_number()
        self.account_type = 'CURRENT'
        self.account_holder = User.query.filter_by(id=account_holder_id).first()

    def save(self):
        db.session.add(self)
        db.session.commit()

    @staticmethod
    def __generate_account_number():
        number = Account.__get_account_number()
        while Account.query.filter_by(account_number=number).count() > 0:
            number = Account.__get_account_number()
        return number

    @staticmethod
    def __get_account_number():
        return int(''.join([str(random.randint(0, 9)) for i in range(10)]))
