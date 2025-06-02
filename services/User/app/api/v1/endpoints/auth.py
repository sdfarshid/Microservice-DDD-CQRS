from typing import Annotated

from fastapi import APIRouter, Request, Depends, HTTPException

from app.domain.user.services.auth_service import AuthService
from app.domain.user.value_objects import Email, Password
from app.utilities.log import handle_exceptions, DebugWaring
from shared.domain.user.commands.auth.auth import RefreshRequest
from shared.domain.user.commands.auth.login_user import LoginUserRequest

router = APIRouter()


AuthServiceDependency = Annotated[AuthService, Depends(AuthService)]


@router.post("/login")
@handle_exceptions
async def login(command: LoginUserRequest,  auth_service: AuthServiceDependency):
    DebugWaring(f"{LoginUserRequest}")
    email_vo = Email(value=command.email)
    password_vo = Password(value=command.password)
    return await auth_service.login(email_vo, password_vo)


@router.post("/refresh")
@handle_exceptions
async def refresh(command: RefreshRequest, auth_service: AuthServiceDependency
):
    return await auth_service.refresh(command.refresh_token)
