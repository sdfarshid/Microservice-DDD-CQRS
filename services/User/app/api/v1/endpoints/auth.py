from typing import Annotated

from fastapi import APIRouter, Request, Depends, HTTPException

from app.domain.user.services.auth_service import AuthService
from app.domain.user.value_objects.Email import Email
from app.domain.user.value_objects.Password import Password

router = APIRouter()


AuthServiceDependency = Annotated[AuthService, Depends(AuthService)]


@router.post("/login")
async def login(
        email: Email,
        password: Password,
        auth_service: AuthServiceDependency
):
    try:
        tokens = await auth_service.login(email, password)
        return tokens
    except ValueError as e:
        raise HTTPException(status_code=401, detail=str(e))


@router.post("/refresh")
async def refresh(
        refresh_token: str,
        auth_service: AuthServiceDependency
):
    try:
        tokens = await auth_service.refresh(refresh_token)
        return tokens
    except ValueError as e:
        raise HTTPException(status_code=401, detail=str(e))