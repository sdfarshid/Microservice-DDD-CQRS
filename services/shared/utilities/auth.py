import jwt
from fastapi import Depends, HTTPException, Header, Request
from fastapi.security import OAuth2PasswordBearer
from rich import status

from shared.config.settings import share_setting

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


def verify_token(token: str = Depends(oauth2_scheme)) -> bool:
    try:
        payload = jwt.decode(token, share_setting.PUBLIC_KEY, algorithms=[share_setting.ALGORITHM])
        return payload
    except jwt.InvalidTokenError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )


def verify_api_key(request: Request):
    api_key = request.headers.get("X-API-Key")
    if api_key != share_setting.GATEWAY_API_KEY:
        raise HTTPException(status_code=403, detail="Invalid API key")
    return api_key


async def get_user_id(x_user_id: str = Header(...)):
    if not x_user_id:
        raise HTTPException(status_code=400, detail="X-User-ID header is required")
    return x_user_id
