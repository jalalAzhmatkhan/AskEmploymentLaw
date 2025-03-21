import traceback
from typing import Annotated, List

from fastapi import APIRouter, Depends, HTTPException, Security
from sqlalchemy.orm import Session

from constants.core import security as security_constants
from constants import general as general_constants
from core.db_connection import database
from core.logger import logger
from models import TblUsers
from schemas import (
    RoleCreate,
    RolesScreenResponse,
    RoleUpdate,
    UserRolesMappingRequest,
    UserRolesResponse,
)
from services import auth_service, role_service

roles_controller = APIRouter()

@roles_controller.get("/all", response_model=List[RolesScreenResponse])
def get_all_roles(
    db: Session = Depends(database.get_postgresql_db),
    *,
    current_user: Annotated[
        TblUsers,
        Security(
            auth_service.get_current_active_user,
            scopes=[security_constants.PERMISSION_READ_ALL_ROLES]
        )
    ]
)->List[RolesScreenResponse]:
    """
    API to get All Roles
    :param db:
    :param current_user:
    :return:
    """
    print(f"Is Active: {current_user.is_active}")
    return role_service.get_all_roles(db=db)

@roles_controller.get("/me", response_model=List[RolesScreenResponse])
def get_current_user_roles(
    db: Session = Depends(database.get_postgresql_db),
    *,
    current_user: Annotated[
        TblUsers,
        Security(
            auth_service.get_current_active_user,
            scopes=[security_constants.PERMISSION_READ_ROLES_ME]
        )
    ]
)->List[RolesScreenResponse]:
    """
    API to get Current User's Role
    :param db:
    :param current_user:
    :return:
    """
    current_user_id = current_user.id
    responses = []
    try:
        responses = role_service.get_roles_by_user_id(db=db, user_id=current_user_id)
    except Exception as e:
        error_msg = traceback.format_exc()
        logger.error(f"get_current_user_roles: {error_msg}", exc_info=True)
        raise HTTPException(
            status_code=general_constants.HTTP_STATUS_INTERNAL_SERVER_ERROR,
            detail=general_constants.HTTP_STATUS_DETAIL_INTERNAL_SERVER_ERROR,
        )

    return responses

@roles_controller.post("/insert", response_model=RolesScreenResponse)
def create_new_role(
    db: Session = Depends(database.get_postgresql_db),
    *,
    data: RoleCreate,
    current_user: Annotated[
        TblUsers,
        Security(
            auth_service.get_current_active_user,
            scopes=[security_constants.PERMISSION_WRITE_ROLES]
        )
    ]
)->RolesScreenResponse:
    """
    API to Create a new Role
    :param db:
    :param data:
    :param current_user:
    :return:
    """
    return role_service.create_new_role(db=db, data=data)

@roles_controller.put("/update", response_model=RolesScreenResponse)
def update_a_role(
    db: Session = Depends(database.get_postgresql_db),
    *,
    role_id: int,
    data: RoleUpdate,
    current_user: Annotated[
        TblUsers,
        Security(
            auth_service.get_current_active_user,
            scopes=[security_constants.PERMISSION_UPDATE_ROLES]
        )
    ]
)->RolesScreenResponse:
    """
    An API to update a role
    :param db:
    :param role_id:
    :param data:
    :param current_user:
    :return:
    """
    return role_service.update_role(db=db, role_id=role_id, update_data=data)

@roles_controller.delete("/delete", response_model=RolesScreenResponse)
def delete_a_role(
    db: Session = Depends(database.get_postgresql_db),
    *,
    role_id: int,
    current_user: Annotated[
        TblUsers,
        Security(
            auth_service.get_current_active_user,
            scopes=[security_constants.PERMISSION_DELETE_ROLES]
        )
    ]
)->RolesScreenResponse:
    """
    An API to delete a Role by role_id
    :param db:
    :param role_id:
    :param current_user:
    :return:
    """
    return role_service.delete_role(db=db, role_id=role_id)

@roles_controller.get("/user_roles/all", response_model=List[UserRolesResponse])
def get_all_userroles_mapping(
    db: Session = Depends(database.get_postgresql_db),
    *,
    current_user: Annotated[
        TblUsers,
        Security(
            auth_service.get_current_active_user,
            scopes=[security_constants.PERMISSION_READ_ALL_USER_ROLES_MAPPING]
        )
    ]
)->List[UserRolesResponse]:
    """
    API to get All User-Roles Mapping
    :param db:
    :param current_user:
    :return:
    """
    return role_service.get_all_userroles_map(db=db)

@roles_controller.get("/user_roles/user", response_model=UserRolesResponse)
def get_userroles_mapping_by_user_id(
    db: Session = Depends(database.get_postgresql_db),
    *,
    id: int,
    current_user: Annotated[
        TblUsers,
        Security(
            auth_service.get_current_active_user,
            scopes=[security_constants.PERMISSION_READ_SPECIFIC_USER_ROLES_MAPPING]
        )
    ]
)->UserRolesResponse:
    """
    API to Get User-Roles mapping by user_id
    :param db:
    :param id:
    :param current_user:
    :return:
    """
    return role_service.get_userroles_map_by_user_id(db=db, user_id=id)

@roles_controller.post("/user_roles", response_model=UserRolesResponse)
def insert_user_roles_mapping(
    db: Session = Depends(database.get_postgresql_db),
    *,
    data: UserRolesMappingRequest,
    current_user: Annotated[
        TblUsers,
        Security(
            auth_service.get_current_active_user,
            scopes=[security_constants.PERMISSION_WRITE_USER_ROLES_MAPPING]
        )
    ]
)->UserRolesResponse:
    """
    API to Create User-Roles mapping
    :param db:
    :param data:
    :param current_user:
    :return:
    """
    return role_service.user_roles_map(db=db, request_data=data)

@roles_controller.delete("/user_roles", response_model=UserRolesResponse)
def delete_user_roles_mapping(
    db: Session = Depends(database.get_postgresql_db),
    *,
    id: int,
    current_user: Annotated[
        TblUsers,
        Security(
            auth_service.get_current_active_user,
            scopes=[security_constants.PERMISSION_DELETE_USER_ROLES_MAPPING]
        )
    ]
)->UserRolesResponse:
    """
    API to Delete User-Roles Mapping by its ID
    :param db:
    :param id:
    :param current_user:
    :return:
    """
    return role_service.delete_user_roles_map(db=db, id=id)
