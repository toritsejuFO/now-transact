from app.utility import Response
from app.services import authentication_required, AccountService

@authentication_required
def post(payload, subscriber):
    account = AccountService.create_account(payload, subscriber)
    return Response.success(account), 201

@authentication_required
def get(account_id, subscriber):
    account = AccountService.get_account(account_id, subscriber)
    return Response.success(account), 200

@authentication_required
def put(account_id, payload, subscriber):
    account = AccountService.update_account(account_id, payload, subscriber)
    return Response.success(account), 200

@authentication_required
def delete(account_id, subscriber):
    account = AccountService.delete_account(account_id, subscriber)
    return Response.success(account), 200
