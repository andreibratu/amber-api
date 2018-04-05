from services.UserService import UserService


class SecurityService:
    @staticmethod
    def authenticate(username, password):
        user = UserService.get_user_by_email(username)
        print(user)
        if user and user.check_password(password):
            return user

    @staticmethod
    def identity(payload):
        return UserService.get_user_by_id(payload['identity'])
