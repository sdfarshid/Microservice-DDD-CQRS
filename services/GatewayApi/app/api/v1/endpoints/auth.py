from fastapi import APIRouter, Depends
from app.config.config import settings
from app.utilities.helper import handle_exceptions, call_api

from app.utilities.log import DebugWaring
from shared.domain.user.commands.auth.auth import RefreshRequest
from shared.domain.user.commands.auth.login_user import LoginUserRequest

router = APIRouter(tags=["user"])
User_BASE_URL = settings.get_service_url("user")


@router.post("/login")
@handle_exceptions
async def login(command: LoginUserRequest):
    DebugWaring(f"{User_BASE_URL}/login",)
    return await call_api(
        method="POST",
        endpoint=f"{User_BASE_URL}/login",
        json_data=command.model_dump()
    )


@router.post("/refresh")
@handle_exceptions
async def refresh(command: RefreshRequest):
    return await call_api(
        method="POST",
        endpoint=f"{User_BASE_URL}/refresh",
        json_data=command.model_dump()
    )
