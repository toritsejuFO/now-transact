from app.services import UserService
from app.utility import Response

def post(payload):
    new_user = UserService.create_user(payload)
    return Response.success(new_user), 201

