import os
import functools
from datetime import datetime, timedelta
from werkzeug.security import check_password_hash
import jwt
from flask import request

from app.schemas import auth_schema
from app.dao import UserDao
from app.exceptions import AppException

JWT_SECRET_KEY = os.getenv('JWT_SECRET_KEY')

class AuthService:
    def get_auth_token(payload):
        schema = auth_schema.load(payload)
        user = UserDao.find_user_by(id=schema['user_id'])

        if not user:
            raise AppException('Invalid auth details', 401)

        if not check_password_hash(user.password, schema['password']):
            raise AppException('Invalid auth details', 401)

        sub = {
            'id': user.id,
            'email': user.email
        }
        token = AuthService.__encode_token(sub)
        return token

    def __encode_token(sub=None, expiry=datetime.utcnow() + timedelta(days=1)):
        if sub is None:
            raise AppException('Invalid subscriber payload')

        try:
            payload = {
                'sub': sub,
                'exp': expiry,
                'iat': datetime.utcnow()
            }
            return jwt.encode(payload, JWT_SECRET_KEY, algorithm='HS256')
        except Exception as e:
            raise AppException('Internal Server Error', 500, e)

    def decode_token(token=None):
        try:
            payload = jwt.decode(token, JWT_SECRET_KEY, algorithms=['HS256'])
            return payload['sub']
        except jwt.ExpiredSignatureError:
            raise AppException('Expired token. Kindly log in again', 403)
        except jwt.InvalidTokenError:
            raise AppException('Invalid token. Kindly log in again', 403)


def authentication_required(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        if 'x-auth-token' not in request.headers.keys(lower=True):
            raise AppException('x-auth-token is required in header')

        auth_token = request.headers.get('x-auth-token')
        if not auth_token or auth_token is None:
            raise AppException('Invalid x-auth-token', 403)

        subscriber = AuthService.decode_token(token=auth_token)
        return func(*args, **kwargs, subscriber=subscriber)
    return wrapper
