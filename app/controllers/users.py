from app.services import UserService
from app.utility import Response

def post(payload):
    new_user = UserService.create_user(payload)
    return Response.success(new_user), 201

def get(user_id):
    user = UserService.get_user(user_id)
    return Response.success(user), 200

def put(user_id, payload):
    user = UserService.update_user(user_id, payload)
    return Response.success(user), 200
