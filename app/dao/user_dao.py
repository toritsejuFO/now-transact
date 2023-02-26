from app.models import User

class UserDao:
    @staticmethod
    def create_user(schema_payload):
        new_user = User(**schema_payload)
        new_user.save()
        return new_user

    def find_user_by_id(user_id):
        return User.query.filter(User.id == user_id).first()
    
    @staticmethod
    def user_exist(schema):
        email = schema['email']
        phonenumber = schema['phonenumber']
        user_count = User.query.filter((User.email==email) | (User.phonenumber==phonenumber)).count()
        return user_count > 0