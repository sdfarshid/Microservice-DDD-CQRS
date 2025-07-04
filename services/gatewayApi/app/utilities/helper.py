from functools import wraps
from typing import Optional
import httpx
from fastapi import HTTPException
from app.utilities.log import DebugError, DebugWaring
from shared.config.settings import share_setting


async def call_api(
    method: str,
    endpoint: str,
    json_data: Optional[dict] = None,
    params: Optional[dict] = None,
    timeout: float = 10.0
):
    full_url = f"{endpoint.lstrip('/')}"
    headers = {"X-API-Key": share_setting.GATEWAY_API_KEY}

    try:
        async with httpx.AsyncClient() as client:
            response = await client.request(
                url=full_url,
                method=method.upper(),
                json=json_data,
                params=params,
                timeout=timeout,
                headers=headers
            )
            response.raise_for_status()
            return response.json()

    except httpx.HTTPStatusError as e:
        try:
            error_detail = e.response.json()
        except Exception:
            error_detail = e.response.text

        DebugError(f"HTTP {e.response.status_code} from {full_url}: {error_detail}")
        raise HTTPException(
            status_code=e.response.status_code,
            detail=error_detail
        )

    except httpx.RequestError as e:
        DebugError(f"Network error occurred: {e} - {full_url}")
        raise HTTPException(status_code=502, detail="Gateway: Network error")

    except Exception as e:
        DebugError(f"Unexpected error occurred: {e} - {full_url}")
        raise HTTPException(status_code=500, detail="Gateway: Internal error")


def handle_exceptions(func):
    @wraps(func)
    async def wrapper(*args, **kwargs):
        try:
            return await func(*args, **kwargs)
        except ValueError as value_error:
            raise HTTPException(status_code=404, detail=str(value_error))
        except HTTPException as http_error:
            raise http_error
        except Exception as error:
            DebugError(f"Error in {func.__name__}: {error}")
            raise HTTPException(status_code=500, detail="Internal server error")

    return wrapper
