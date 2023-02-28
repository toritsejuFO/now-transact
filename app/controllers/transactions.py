from app.utility import Response
from app.services import authentication_required, TransactionService

@authentication_required
def post(account_id, payload, subscriber):
    transaction = TransactionService.execute(account_id, payload, subscriber)
    return Response.success(transaction), 201
