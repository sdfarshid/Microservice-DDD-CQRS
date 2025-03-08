import uuid
import jwt
import os
from datetime import timedelta, datetime
from pydantic import BaseModel

from app.infrastructure.config import settings

BASE_PATH = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
print(f"Base Path: {BASE_PATH}")

PRIVATE_KEY_PATH = settings.PRIVATE_KEY_PATH
PUBLIC_KEY_PATH = settings.PUBLIC_KEY_PATH

with open(os.path.join(BASE_PATH, PRIVATE_KEY_PATH), "r") as f:
    PRIVATE_KEY = f.read()
with open(os.path.join(BASE_PATH, PUBLIC_KEY_PATH), "r") as f:
    PUBLIC_KEY = f.read()


ALGORITHM = "RS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30
REFRESH_TOKEN_EXPIRE_DAYS = 7


class TokenData(BaseModel):
    email: str
    user_id: str
    roles: list[str]
    permissions: list[str]


def create_access_token(to_encode: TokenData, expires_delta: timedelta = None):
    data_dict = to_encode.model_dump()
    expire = datetime.utcnow() + (expires_delta or timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES))
    data_dict.update({"exp": expire, "type": "access", "iss": "user-service"})
    encoded_jwt = jwt.encode(data_dict, PRIVATE_KEY, algorithm=ALGORITHM)
    return encoded_jwt


def create_refresh_token(to_encode: TokenData, expires_delta: timedelta = None):
    data_dict = to_encode.model_dump()
    expire = datetime.utcnow() + (expires_delta or timedelta(days=REFRESH_TOKEN_EXPIRE_DAYS))
    data_dict.update({"exp": expire, "type": "refresh", "iss": "user-service"})
    encoded_jwt = jwt.encode(data_dict, PRIVATE_KEY, algorithm=ALGORITHM)
    return encoded_jwt


def verify_token(token: str):
    try:
        payload = jwt.decode(token, PUBLIC_KEY, algorithms=[ALGORITHM])
        return payload
    except jwt.InvalidTokenError:
        return None
