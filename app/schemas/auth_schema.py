from marshmallow import Schema, EXCLUDE, validates, validates_schema, ValidationError, fields

class AuthSchema(Schema):
    class Meta:
        unknown = EXCLUDE

    user_id = fields.Integer(required=True, error_messages={'required': 'user_id is required'})
    password = fields.String(required=True, error_messages={'required': 'password is required'})

    @validates('user_id')
    def validate_user_id(self, value):
        self.__validate_empty('user_id', value)

    @validates('password')
    def validate_password(self, value):
        self.__validate_empty('password', value)

    def __validate_empty(self, field, value):
        if not value:
            raise ValidationError(f'{field} cannot be empty')

auth_schema = AuthSchema()
