from marshmallow import Schema, EXCLUDE, validates, ValidationError, fields

class AccountSchema(Schema):
    class Meta:
        unknown = EXCLUDE

    id = fields.Integer()
    account_name = fields.String(required=True, error_messages={'required': 'account_name is required'})
    account_balance = fields.String()
    account_number = fields.Integer()
    account_type = fields.String()
    account_holder_id = fields.Integer()
    created_at = fields.DateTime()
    updated_at = fields.DateTime()

    @validates('account_name')
    def validate_account_name(self, value):
        if not value:
            raise ValidationError('account_name cannot be empty')

account_schema = AccountSchema()
