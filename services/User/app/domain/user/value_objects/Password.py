from pydantic import BaseModel, field_validator
from pydantic_core import core_schema


class Password(BaseModel):
    value: str

    @field_validator('value')
    def validate_password(cls, enter_value):
        if len(enter_value) < 8:
            raise ValueError('The password must be at least 8 characters long')
        return enter_value
