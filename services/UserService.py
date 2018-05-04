from app.models import User, Interest
from app.extensions import db


class UserService:
    @staticmethod
    def get_user_by_id(user_id):
        return User.query.filter_by(id=user_id).first()

    @staticmethod
    def get_user_by_email(email):
        return User.query.filter_by(email=email).first()

    @staticmethod
    def register_user(email, password):
        already_registered_user = User.query.filter_by(email=email).first()
        if already_registered_user:
            return None
        new_user = User(first_name=None, given_name=None, age=None,
                        bio=None, email=email, password=password)
        db.session.add(new_user)
        db.session.commit()
        return new_user

    @staticmethod
    def update_user(user_id, age, bio, first_name, given_name, interests):
        def parse_interests():
            return [Interest(label=option.get('label'), category=interest.get('category'))
                    for key, interest in interests.items() for option in interest.get('options')]

        user = User.query.get(user_id)
        if not user:
            return None
        user.age = age
        user.bio = bio
        user.first_name = first_name
        user.given_name = given_name
        user.interests = parse_interests(interests)
        user.first_time = False
        db.session.commit()
        return user

    @staticmethod
    def get_user_busy_times(user_id):
        user = UserService.get_user_by_id(user_id)
        return [event.busytime for event in user.events]
