from app.utility import Response
from app.services import authentication_required, TransactionService

@authentication_required
def post(account_id, payload, subscriber):
    transaction = TransactionService.execute(account_id, payload, subscriber)
    return Response.success(transaction), 201

@authentication_required
def search(account_id, subscriber, offset=0, limit=10, description=None):
    transactions, total = TransactionService.search(account_id, subscriber, offset, limit, description)
    extra_dict = {
        'pagination': {
            'offset': offset,
            'limit': limit,
            'total': total,
        }
    }
    return Response.success(transactions, extra_dict), 200
