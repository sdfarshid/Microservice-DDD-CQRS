from typing import Annotated

from fastapi import APIRouter, Depends

from app.domain import Password, Email
from app.domain.user.services.user_service import UserService
from app.utilities.log import handle_exceptions
from shared.domain.user.commands.user.create_user import CreateUserRequest
from shared.mixins import PaginationParams, get_pagination_params

router = APIRouter()

UserServiceDependency = Annotated[UserService, Depends(UserService)]


@router.get("/users")
@handle_exceptions
async def get_users(user_service: UserServiceDependency,
                    pagination: PaginationParams = Depends(get_pagination_params)):
    return await user_service.list_users(pagination)


@router.post("/register")
@handle_exceptions
async def register(command: CreateUserRequest, user_service: UserServiceDependency):
    email_vo = Email(value=command.email)
    password_vo = Password(value=command.password)
    user = await user_service.create_user(email_vo, password_vo)
    return {"message": "User created successfully", "data": user}
