from app.models import User
from app import db

class UserDao:
    def create_user(schema):
        new_user = User(**schema)
        new_user.save()
        return new_user

    def find_user_by(**kwargs):
        return User.query.filter_by(**kwargs).first()

    def update_user(user_id, schema):
        existing_user = User.query.filter(User.id == user_id).first()
        existing_user.firstname = schema['firstname']
        existing_user.lastname = schema['lastname']
        existing_user.email = schema['email']
        existing_user.phonenumber = schema['phonenumber']
        existing_user.save()
        return existing_user
    
    def delete_user(user_to_delete):
        db.session.delete(user_to_delete)
        db.session.commit()

    def get_user_count_by_or(email, phonenumber):
        user_count = User.query.filter((User.email==email) | (User.phonenumber==phonenumber)).count()
        return user_count

    def get_users_by_or(email, phonenumber):
        users = User.query.filter((User.email==email) | (User.phonenumber==phonenumber)).all()
        return users
    
    def rollback():
        db.session.rollback()
