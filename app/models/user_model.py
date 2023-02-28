from app import db

class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    firstname = db.Column(db.String, nullable=False)
    lastname = db.Column(db.String, nullable=False)
    email = db.Column(db.String, nullable=False, unique=True)
    phonenumber = db.Column(db.String, nullable=False, unique=True)
    password = db.Column(db.String, nullable=False)
    account = db.relationship(
        'Account',
        backref='account_holder',
        cascade="all, delete, delete-orphan",
        single_parent=True
    )

    def __init__(self, firstname=None, lastname=None, email=None, phonenumber=None, password=None):
        self.firstname = firstname.title()
        self.lastname = lastname.title()
        self.email = email.lower()
        self.phonenumber = phonenumber
        self.password = password

    def save(self):
        db.session.add(self)
