from pydantic import EmailStr, BaseModel


class LoginUserRequest(BaseModel):
    email: EmailStr
    password: str


class LoginUserCommand:
    def __init__(self, email: EmailStr, password: str):
        self.email = email
        self.password = password
