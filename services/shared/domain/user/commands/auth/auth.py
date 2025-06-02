from pydantic import BaseModel


class RefreshRequest(BaseModel):
    refresh_token: str


class RefreshTokenCommand:
    def __init__(self, refresh_token: str):
        self.refresh_token = refresh_token
