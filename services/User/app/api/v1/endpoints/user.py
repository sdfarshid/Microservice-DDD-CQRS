from typing import Annotated

from fastapi import APIRouter, Request, Depends, HTTPException
from pydantic import EmailStr, BaseModel

from ....domain.mixins.pagination import PaginationParams, get_pagination_params
from ....domain.user.services.user_service import UserService
from ....domain.user.value_objects.Email import Email
from ....domain.user.value_objects.Password import Password
from ....utilities.log import logger

router = APIRouter()

UserServiceDependency = Annotated[UserService, Depends(UserService)]


@router.get("/users")
async def get_users(user_service: UserServiceDependency,
                    pagination: PaginationParams = Depends(get_pagination_params)):
    return await user_service.list_users(pagination)


@router.post("/register")
async def register(email: Email, password: Password, user_service: UserServiceDependency):
    email_vo = email
    password_vo = password
    try:
        user = await user_service.create_user(email_vo, password_vo)
        return {"message": "User created successfully", "data": user}
    except Exception as error:
        logger.error(f"Error: {error}", exc_info=True)
        raise HTTPException(status_code=500, detail="Internal Server Error")
