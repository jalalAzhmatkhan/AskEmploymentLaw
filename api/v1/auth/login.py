from datetime import timedelta
from typing import Any

from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from constants import general as general_constants
from constants.core import security as security_constants
from core.configs import settings
from core.db_connection import database
from core.security import create_access_token
from repositories.crud_tbl_userroles import crud_tbl_userroles
from schemas.dto import responses
from services import auth_service

login_controller = APIRouter()

@login_controller.post("/login")
def login(
    db: Session = Depends(database.get_postgresql_db),
    form_data: OAuth2PasswordRequestForm = Depends()
)->Any:
    """
    Login controller
    :param db:
    :param form_data:
    :return:
    """
    authenticated_user = auth_service.authenticate_user(
        db,
        form_data.username,
        form_data.password
    )
    if not authenticated_user:
        raise HTTPException(
            status_code=general_constants.HTTP_STATUS_ERROR_BAD_REQUEST,
            detail=general_constants.HTTP_STATUS_DETAIL_INCORRECT_USERNAME_PASSWORD,
        )
    elif not authenticated_user.is_active:
        raise HTTPException(
            status_code=general_constants.HTTP_STATUS_ERROR_BAD_REQUEST,
            detail=general_constants.HTTP_STATUS_DETAIL_INACTIVE_USER,
        )
    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    logged_in_user_roles = crud_tbl_userroles.get_by_user_id(
        db=db,
        user_id=authenticated_user.id,
    )
    logged_in_user_role_ids = [logged_in_user_role.role_id for logged_in_user_role in logged_in_user_roles]
    if len(logged_in_user_role_ids) == 0:
        raise HTTPException(
            status_code=general_constants.HTTP_STATUS_ERROR_BAD_REQUEST,
            detail=general_constants.HTTP_STATUS_DETAIL_NO_ROLES_FOUND,
        )
    role_permissions = crud_tbl_userroles.get_user_role_permissions_by_user_id(
        db=db,
        user_id=authenticated_user.id
    )
    user_permissions = [role_permission.permissions for role_permission in role_permissions]
    if len(user_permissions) > 0:
        user_permissions = list(set(user_permissions[0]))
    return responses.LoginResponse(
        access_token=create_access_token(
            subject=str(authenticated_user.id),
            role_id=logged_in_user_role_ids,
            expires_delta=access_token_expires,
            permissions=user_permissions,
        ),
        token_type=security_constants.BEARER_TOKEN
    )
