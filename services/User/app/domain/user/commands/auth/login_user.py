from app.domain.user.value_objects.Email import Email
from app.domain.user.value_objects.Password import Password


class LoginUserCommand:
    def __init__(self, email: Email, password: Password):
        self.email = email
        self.password = password
