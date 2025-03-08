from app.domain.user.value_objects.Email import Email


class GetUserByEmailQuery:
    def __init__(self, email: Email):
        self.email = email
