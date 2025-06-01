from fastapi import Depends, HTTPException, Header, Request

from shared.config.settings import share_setting


async def get_user_id(x_user_id: str = Header(...)):
    if not x_user_id:
        raise HTTPException(status_code=400, detail="X-User-ID header is required")
    return x_user_id


def verify_api_key(request: Request):
    api_key = request.headers.get("X-API-Key")
    if api_key != share_setting.GATEWAY_API_KEY:
        raise HTTPException(status_code=403, detail="Invalid API key")
    return api_key

