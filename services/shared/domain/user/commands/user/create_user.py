from pydantic import BaseModel, EmailStr


class CreateUserRequest(BaseModel):
    email: EmailStr
    password: str


class CreateUserCommand:
    def __init__(self, email: EmailStr, password: str):
        self.email = email
        self.password = password
