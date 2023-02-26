from app.services import AuthService
from app.utility import Response

def post(payload):
    token = AuthService.get_auth_token(payload)
    return Response.success({ 'token': token }), 200
