from werkzeug.security import generate_password_hash, check_password_hash
import bd_repo


class UserLogin:
    def fromDB(self, user_id):
        self.__user = bd_repo.getUserByID(user_id)
        return self

    def create(self, user):
        self.__user = user
        return self

    def is_authenticated(self):
        return True

    def is_active(self):
        return True

    def is_anonymous(self):
        return False

    def get_id(self):
        return str(self.__user[0][0])

    def get_username(self):
        return str(self.__user[0][1])
