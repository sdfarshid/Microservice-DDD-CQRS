import logging
import sys
from functools import wraps
from pathlib import Path

from fastapi import HTTPException

log_dir = Path(__file__).parent.parent / "logs"
log_dir.mkdir(parents=True, exist_ok=True)

logger = logging.getLogger("app")
logger.setLevel(logging.DEBUG)

formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")

file_handler = logging.FileHandler(log_dir / "app.log", encoding="utf-8")
file_handler.setFormatter(formatter)

stream_handler = logging.StreamHandler(sys.stdout)
stream_handler.setFormatter(formatter)

if not logger.hasHandlers():
    logger.addHandler(file_handler)
    logger.addHandler(stream_handler)

logger.debug("Logger initialized!")


def DebugWaring(message: object) -> object:
    logger.debug(f"⚠️⚠️ --  {message}")


def DebugError(message):
    logger.debug(f"🚨️ --  {message}")


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
