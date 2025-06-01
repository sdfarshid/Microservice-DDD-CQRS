from functools import wraps
from typing import Optional

import httpx
from fastapi import HTTPException
from pydantic import ValidationError

from app.utilities.log import DebugError, DebugWaring


async def call_api(
        method: str,
        endpoint: str,
        json_data: Optional[dict] = None,
        params: Optional[dict] = None,
        timeout: float = 10.0
):
    full_url = f"{endpoint.lstrip('/')}"
    DebugWaring(full_url)
    try:
        async with httpx.AsyncClient() as client:
            response = await client.request(
                url=full_url,
                method=method.upper(),
                json=json_data,
                params=params,
                timeout=timeout
            )
            response.raise_for_status()
            return response.json()
    except httpx.HTTPStatusError as e:
        DebugError(f"HTTP status error occurred: {e} - {full_url}")
        raise ValueError(f"HTTP error occurred: {e}")
    except httpx.RequestError as e:
        DebugError(f"Network error occurred: {e} - {full_url}")
        raise ValueError(f"Network error occurred: {e}")
    except ValueError as e:
        DebugError(f"Invalid JSON response: {e} - {full_url}")
        raise ValueError(f"Invalid JSON response: {e}")
    except Exception as e:
        DebugError(f"Unexpected error occurred: {e} - {full_url}")
        raise ValueError(f"Unexpected error: {e}")


def handle_exceptions(func):
    @wraps(func)
    async def wrapper(*args, **kwargs):
        try:
            return await func(*args, **kwargs)
        except ValidationError as ve:
            # Extract Pydantic error messages
            error_messages = [f"{err['msg']}" for err in ve.errors()]
            detail = "; ".join(error_messages)
            DebugError(f"Validation error in {func.__name__}: {detail}")
            raise HTTPException(status_code=422, detail=detail)
        except ValueError as value_error:
            DebugError(f"Value error in {func.__name__}: {value_error}")
            raise HTTPException(status_code=404, detail=str(value_error))
        except HTTPException as http_error:
            raise http_error
        except Exception as error:
            DebugError(f"Error in {func.__name__}: {error}")
            raise HTTPException(status_code=500, detail="Internal server error")

    return wrapper
