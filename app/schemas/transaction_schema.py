from marshmallow import Schema, EXCLUDE, validates, ValidationError, fields

from app.utility import Money, TransactionType

def required_str(field):
    return fields.String(required=True, error_messages={'required': f'{field} is required'})

class TransactionSchema(Schema):
    class Meta:
        unknown = EXCLUDE

    id = fields.Integer()
    transaction_id = fields.String()
    transaction_amount = required_str('transaction_amount')
    transaction_description = required_str('transaction_description')
    transaction_type = required_str('transaction_type')
    transaction_status = fields.String()
    entry_date = fields.DateTime()
    created_at = fields.DateTime()
    updated_at = fields.DateTime()

    @validates('transaction_amount')
    def validate_transaction_amount(self, value):
        self.__validate_empty('transaction_amount', value)
        if value[-3:][0] != '.': # nice little trick
            raise ValidationError('transaction_amount must be to 2 decimal places')
        if len(value.split('.')[0]) > 10:
            raise ValidationError('transaction_amount above allowed limit')
        if Money(value).amount < 0:
            raise ValidationError('transaction_amount cannot be negative')

    @validates('transaction_description')
    def validate_transaction_description(self, value):
        self.__validate_empty('transaction_description', value)

    @validates('transaction_type')
    def validate_transaction_type(self, value):
        self.__validate_empty('transaction_type', value)
        if value not in [TransactionType.DEPOSIT, TransactionType.WITHDRAWAL]:
            raise ValidationError('Invalid transaction_type, must be either DEPOSIT or WITHDRAWAL')

    def __validate_empty(self, field, value):
        if not value:
            raise ValidationError(f'{field} cannot be empty')

transaction_schema = TransactionSchema()
