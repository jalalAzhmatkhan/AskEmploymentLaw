from typing import Annotated, List

from fastapi import APIRouter, Depends, Security
from sqlalchemy.orm import Session

from constants.core import security as security_constants
from core.db_connection import database
from models import TblUsers
from schemas import PermissionsCreateRequest, PermissionsUpdateRequest, PermissionsResponse
from services import auth_service, permission_service

permissions_controller = APIRouter()

@permissions_controller.get("/all")
def get_all_permissions(
    db: Session = Depends(database.get_postgresql_db),
    *,
    current_user: Annotated[
        TblUsers,
        Security(
            auth_service.get_current_active_user,
            scopes=[security_constants.PERMISSION_READ_ALL_PERMISSIONS]
        )
    ]
)->List[PermissionsResponse]:
    """
    API to get All Permissions
    :param current_user:
    :param db:
    :return:
    """
    return permission_service.get_all_permissions(db=db)

@permissions_controller.get("/me")
def get_current_user_permissions(
    db: Session = Depends(database.get_postgresql_db),
    *,
    current_user: Annotated[
        TblUsers,
        Security(
            auth_service.get_current_active_user,
            scopes=[security_constants.PERMISSION_READ_PERMISSIONS_ME]
        )
    ]
)->List[PermissionsResponse]:
    """
    API to get current user's Permissions
    :param current_user:
    :param db:
    :return:
    """
    return permission_service.get_user_permissions(db=db, user_id=current_user.id)

@permissions_controller.get("/user/{user_id}")
def get_current_user_permissions(
    db: Session = Depends(database.get_postgresql_db),
    *,
    user_id: int,
    current_user: Annotated[
        TblUsers,
        Security(
            auth_service.get_current_active_user,
            scopes=[security_constants.PERMISSION_READ_USER_PERMISSIONS]
        )
    ]
)->List[PermissionsResponse]:
    """
    API to get a specific user's Permissions
    :param user_id:
    :param current_user:
    :param db:
    :return:
    """
    return permission_service.get_user_permissions(db=db, user_id=user_id)

@permissions_controller.post("/insert", response_model=PermissionsResponse)
def create_new_permission(
    db: Session = Depends(database.get_postgresql_db),
    *,
    data: PermissionsCreateRequest,
    current_user: Annotated[
        TblUsers,
        Security(
            auth_service.get_current_active_user,
            scopes=[security_constants.PERMISSION_WRITE_PERMISSIONS]
        )
    ]
) -> PermissionsResponse:
    """
    API to create a new permission
    :param db:
    :param data:
    :param current_user:
    :return:
    """
    return permission_service.create_a_permission(db=db, data=data)

@permissions_controller.put("/update", response_model=PermissionsResponse)
def update_permission(
    db: Session = Depends(database.get_postgresql_db),
    *,
    permission_id: int,
    data: PermissionsUpdateRequest,
    current_user: Annotated[
        TblUsers,
        Security(
            auth_service.get_current_active_user,
            scopes=[security_constants.PERMISSION_WRITE_PERMISSIONS]
        )
    ]
) -> PermissionsResponse:
    """
    API to create a new permission
    :param permission_id:
    :param db:
    :param data:
    :param current_user:
    :return:
    """
    return permission_service.update_a_permission(
        db=db,
        permission_id=permission_id,
        data=data
    )

@permissions_controller.delete("/delete", response_model=PermissionsResponse)
def delete_permission(
    db: Session = Depends(database.get_postgresql_db),
    *,
    permission_id: int,
    current_user: Annotated[
        TblUsers,
        Security(
            auth_service.get_current_active_user,
            scopes=[security_constants.PERMISSION_WRITE_PERMISSIONS]
        )
    ]
)->PermissionsResponse:
    """
    API to Delete a Permission and all the relationships with Roles
    :param db:
    :param permission_id:
    :param current_user:
    :return:
    """
    return permission_service.delete_a_permission(db=db, permission_id=permission_id)
