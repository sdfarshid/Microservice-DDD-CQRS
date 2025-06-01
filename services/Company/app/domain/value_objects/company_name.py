from pydantic import BaseModel, field_validator


class CompanyName(BaseModel):
    value: str
    
    def __init__(self, value: str):
        super().__init__(value=value)
    
    @field_validator('value')
    @classmethod
    def validate_name(cls, value: str) -> str:
        if not value:
            raise ValueError("Company name cannot be empty")
        if len(value) < 2:
            raise ValueError("Company name must be at least 2 characters long")
        if len(value) > 100:
            raise ValueError("Company name must be less than 100 characters")
        return value
        
    def __str__(self) -> str:
        return self.value
