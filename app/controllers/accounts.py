from app.utility import Response
from app.services import authentication_required, AccountService

@authentication_required
def post(payload, subscriber):
    account = AccountService.create_account(payload, subscriber)
    return Response.success(account), 201

@authentication_required
def search(subscriber):
    accounts = AccountService.get_accounts(subscriber)
    return Response.success(accounts), 200
