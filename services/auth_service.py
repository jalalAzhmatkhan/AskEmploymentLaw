from typing import Annotated, Optional, Union

from fastapi import Depends, HTTPException, Security
from fastapi.security import SecurityScopes
import jwt
from jwt.exceptions import InvalidTokenError
from pydantic import ValidationError
from sqlalchemy.orm import Session

from constants import general as general_constants
from constants.core import security as security_constants
from constants.services import auth as auth_constants
from core.configs import settings
from core.db_connection import database
from core.logger import logger
from core.security import oauth2_scheme, verify_password
from models.tbl_users import TblUsers
from repositories import crud_tbl_users, crud_tbl_userroles
from schemas.core import security as security_schemas

def authenticate_user(
    db: Session = Depends(database.get_postgresql_db),
    *,
    username: str,
    password: str
)->Union[Optional[TblUsers], bool]:
    """
    Function to authenticate the user by the username and password
    :param db:
    :param username:
    :param password:
    :return:
    """
    user = crud_tbl_users.get_by_email(db, email=username)
    if not user:
        return False
    if not verify_password(password, user.hashed_password):
        return False
    return user

async def get_current_user(
    security_scopes: SecurityScopes,
    token: str = Depends(oauth2_scheme),
    db: Session = Depends(database.get_postgresql_db),
)->Optional[TblUsers]:
    """
    Function to get the current user
    :param db:
    :param security_scopes:
    :param token:
    :return:
    """
    if security_scopes.scopes:
        authenticate_value = f'{security_constants.BEARER_TOKEN} scope="{security_scopes.scope_str}"'
    else:
        authenticate_value = security_constants.BEARER_TOKEN
    credentials_exception = HTTPException(
        status_code=general_constants.HTTP_STATUS_ERROR_UNAUTHORIZED,
        detail=general_constants.HTTP_STATUS_DETAIL_BAD_CREDENTIALS,
        headers={general_constants.HEADERS_WWW_AUTHENTICATE: authenticate_value }
    )

    try:
        payload = jwt.decode(
            token,
            settings.SECRET_KEY,
            algorithms=[security_constants.ENCODING_ALGORITHM]
        )
        user_id = payload.get("sub")
        if user_id is None:
            raise HTTPException(
                status_code=general_constants.HTTP_STATUS_ERROR_UNAUTHORIZED,
                detail=general_constants.HTTP_STATUS_DETAIL_BAD_CREDENTIALS,
                headers={general_constants.HEADERS_WWW_AUTHENTICATE: authenticate_value }
            )
        token_data = security_schemas.AccessTokenDataSchema(
            exp=payload.get("exp"),
            sub=user_id,
            role_ids=payload.get("role_ids"),
            scopes=payload.get("scopes")
        )
    except (InvalidTokenError, ValidationError) as exc:
        logger.error(f"get_current_user: {exc}", exc_info=True)
        raise credentials_exception from exc

    user = crud_tbl_users.get_by_id(db, id=user_id)
    if user is None:
        raise credentials_exception
    for scope in security_scopes.scopes:
        if scope not in token_data.scopes:
            raise HTTPException(
                status_code=general_constants.HTTP_STATUS_ERROR_UNAUTHORIZED,
                detail=general_constants.HTTP_STATUS_DETAIL_FORBIDDEN,
                headers={general_constants.HEADERS_WWW_AUTHENTICATE: authenticate_value}
            )
    return user

async def get_current_active_user(
    current_user: TblUsers = Security(get_current_user, scopes=[security_constants.PERMISSION_READ_ME])
)->Optional[TblUsers]:
    """
    Function to get the current active user
    :param current_user:
    :return:
    """
    if not current_user.is_active:
        raise HTTPException(
            status_code=general_constants.HTTP_STATUS_ERROR_BAD_REQUEST,
            detail=general_constants.HTTP_STATUS_DETAIL_INACTIVE_USER
        )
    return current_user

async def get_current_active_superuser(
    current_user: TblUsers = Depends(get_current_active_user)
)->Optional[TblUsers]:
    """
    Function to get the current active user
    :param db:
    :param current_user:
    :return:
    """
    db = database.SessionLocal()
    current_roles = crud_tbl_userroles.get_user_role_name_by_user_id(db=db, user_id=current_user.id)
    if len(current_roles) < 1:
        raise HTTPException(
            status_code=general_constants.HTTP_STATUS_ERROR_UNAUTHORIZED,
            detail=general_constants.HTTP_STATUS_DETAIL_NO_ROLES_FOUND,
        )
    role_names = [role.role_name for role in current_roles]
    if auth_constants.ROLE_SUPERADMIN not in role_names:
        raise HTTPException(
            status_code=general_constants.HTTP_STATUS_ERROR_UNAUTHORIZED,
            detail=general_constants.HTTP_STATUS_DETAIL_NOT_ENOUGH_PRIVILEGES,
        )
    return current_user
