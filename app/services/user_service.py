from werkzeug.security import generate_password_hash

from app.dao import UserDao
from app.schemas import user_schema
from app.exceptions import AppException
from app import db

class UserService:
    @staticmethod
    def create_user(payload):
        schema = user_schema.load(payload)

        if UserDao.user_exist(schema):
            raise AppException('Try again with another email or phonenumber', 409)

        try:
            schema = UserService.hash_password(schema)
            new_user = UserDao.create_user(schema)
            return UserService.clean_password(user_schema.dump(new_user))
        except Exception as ex:
            db.session.rollback()
            raise AppException('Failed to create user', 500, ex)
        
    @staticmethod
    def clean_password(schema):
        if 'password' in schema:
            del schema['password']
        return schema

    @staticmethod
    def hash_password(schema):
        if 'password' in schema:
            schema['password'] = generate_password_hash(schema['password'])
        return schema
