from werkzeug.security import generate_password_hash

from app.dao import UserDao
from app.schemas import user_schema, update_user_schema
from app.exceptions import AppException

class UserService:
    def create_user(payload):
        schema = user_schema.load(payload)
        if UserDao.get_user_count_by_or(email=schema['email'], phonenumber=schema['phonenumber']) > 0:
            raise AppException('Try again with another email or phonenumber', 409)

        try:
            schema['password'] = UserService.hash_password(schema['password'])
            new_user = UserDao.create_user(schema)
            return UserService.clean_password(user_schema.dump(new_user))
        except Exception as ex:
            UserDao.rollback()
            raise AppException('Failed to create user', 500, ex)

    def get_user(user_id):
        user = UserDao.find_user_by(id=user_id)
        if user is None:
            raise AppException('User not found', 404)

        return UserService.clean_password(user_schema.dump(user))

    def update_user(user_id, payload):
        update_schema = update_user_schema.load(payload)

        user_to_update =  UserDao.find_user_by(id=user_id)
        if not user_to_update:
            raise AppException('User not found', 404)

        # Do not allow user update to email or phonenumber belonging to another user
        existing_users =  UserDao.get_users_by_or(email=payload['email'], phonenumber=payload['phonenumber'])
        if len(existing_users) > 0:
            error_msg = 'Try again with another email or phonenumber'
            if len(existing_users) > 1:
                raise AppException(error_msg, 409)
            if existing_users[0].id is not user_to_update.id:
                raise AppException(error_msg, 409)

        try:
            updated_user = UserDao.update_user(user_id, update_schema)
            return UserService.clean_password(user_schema.dump(updated_user))
        except Exception as ex:
            UserDao.rollback()
            raise AppException('Failed to update user', 500, ex)

    def delete_user(user_id):
        user_to_delete = UserDao.find_user_by(id=user_id)
        if not user_to_delete:
            raise AppException('User not found', 404)

        UserDao.delete_user(user_to_delete)
        return UserService.clean_password(user_schema.dump(user_to_delete))

    def clean_password(schema):
        if 'password' in schema:
            del schema['password']
        return schema

    def hash_password(password):
        return generate_password_hash(password)
