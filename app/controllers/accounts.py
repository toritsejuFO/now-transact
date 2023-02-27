from app.utility import Response
from app.services import authentication_required, AccountService

@authentication_required
def post(payload, subscriber):
    account = AccountService.create_account(payload, subscriber)
    return Response.success(account), 200
