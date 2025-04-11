import jwt
import os
from datetime import timedelta, datetime
from pydantic import BaseModel

from app.config.config import settings


BASE_PATH = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

PRIVATE_KEY_PATH = settings.PRIVATE_KEY_PATH
PUBLIC_KEY_PATH = settings.PUBLIC_KEY_PATH

private_key_full_path = os.path.join(BASE_PATH, PRIVATE_KEY_PATH)
public_key_full_path = os.path.join(BASE_PATH, PUBLIC_KEY_PATH)

if not os.path.exists(private_key_full_path):
    raise FileNotFoundError(f"Private key file not found at: {private_key_full_path}")
if not os.path.exists(public_key_full_path):
    raise FileNotFoundError(f"Public key file not found at: {public_key_full_path}")



with open(private_key_full_path, "r") as f:
    PRIVATE_KEY = f.read()
with open(public_key_full_path, "r") as f:
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
