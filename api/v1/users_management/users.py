from typing import Any, Annotated

from fastapi import APIRouter, Depends, Form, Security
from pydantic import EmailStr
from sqlalchemy.orm import Session

from constants.core import security as security_constants
from core.db_connection import database
from models import TblUsers
from schemas.dto import responses
from schemas import UserRegistrationRequest
from services import auth_service, user_registration_service

user_management_controller = APIRouter()

@user_management_controller.post(
    "/register",
    response_model=responses.UserRegistrationResponse
)
def register(
    db: Session = Depends(database.get_postgresql_db),
    *,
    user_data: Annotated[UserRegistrationRequest, Form()]
)->Any:
    """
    API for registering a new user
    :param user_data:
    :param db:
    :return:
    """
    return user_registration_service.create_new_user(db=db, obj_req=user_data)

@user_management_controller.get(
    "/detail/me",
    response_model=responses.UserRegistrationResponse
)
def get_current_user_detail(
    current_user: Annotated[
        TblUsers,
        Security(
            auth_service.get_current_active_superuser,
            scopes=[security_constants.PERMISSION_READ_ROLES_ME]
        )
    ]
)->Any:
    """
    Get current user's detail
    :param current_user:
    :return:
    """
    return responses.UserRegistrationResponse(
        id=current_user.id,
        full_name=current_user.full_name,
        email=EmailStr(current_user.email),
        is_active=current_user.is_active
    )
