from app import db

class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    firstname = db.Column(db.String, nullable=False)
    lastname = db.Column(db.String, nullable=False)
    email = db.Column(db.String, nullable=False, unique=True)
    phonenumber = db.Column(db.String, nullable=False, unique=True)
    password = db.Column(db.String, nullable=False)

    def __init__(self, firstname=None, lastname=None, email=None, phonenumber=None, password=None):
        self.firstname = firstname.title()
        self.lastname = lastname.title()
        self.email = email
        self.phonenumber = phonenumber
        self.password = password

    def save(self):
        db.session.add(self)
        db.session.commit()
