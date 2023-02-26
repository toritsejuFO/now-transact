import re
from marshmallow import EXCLUDE, validates, ValidationError, fields

from app import ma

def required_str(field):
    return fields.String(required=True, error_messages={'required': f'{field} is required'})

def required_email(field):
    return fields.Email(required=True, error_messages={'required': f'{field} is required'})

class UserSchema(ma.SQLAlchemySchema):
    class Meta:
        unknown = EXCLUDE

    id = fields.Integer()
    firstname = required_str('firstname')
    lastname = required_str('lastname')
    email = required_email('email')
    phonenumber = required_str('phonenumber')
    password = required_str('password')

    @validates('firstname')
    def validate_firstname(self, value):
        self.__validate_empty('firstname', value)
        
    @validates('lastname')
    def validate_lastname(self, value):
        self.__validate_empty('lastname', value)

    @validates('email')
    def validate_email(self, value):
        self.__validate_empty('email', value)

    @validates('phonenumber')
    def validate_phonenumber(self, value):
        self.__validate_empty('phonenumber', value)

    @validates('password')
    def validate_password(self, value):
        self.__validate_empty('password', value)
        if len(value) < 8:
            raise ValidationError('password must be at least 8 characters long')
        if not re.compile(r'(?=.*[a-z])(?=.*[A-Z])(?=.*[0-9])(?=.*[^A-Za-z0-9])').search(value):
            raise ValidationError('password must have at least a lowercase letter, an uppercase letter, a number, and a special character')

    def __validate_empty(self, field, value):
        if not value:
            raise ValidationError(f'{field} cannot be empty')

user_schema = UserSchema()
users_schema = UserSchema(many=True)
