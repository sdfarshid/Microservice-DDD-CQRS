from pydantic import BaseModel, EmailStr, field_validator


class Email(BaseModel):
    value: EmailStr

    def __str__(self):
        return self.value

    @classmethod
    @field_validator('value')
    def validate_email(cls, v):
        return v.lower()
