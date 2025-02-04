from typing import Annotated, List

from fastapi import APIRouter, Depends, Security
from sqlalchemy.orm import Session

from constants.core import security as security_constants
from core.db_connection import database
from models import TblUsers
from schemas import (
    PermissionsCreateRequest,
    PermissionsUpdateRequest,
    PermissionsResponse,
    RolePermissionsMappingRequest,
    RolePermissionsMappingResponse,
    UserRolePermissionsMappingsResponse,
)
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

@permissions_controller.get(
    "/role_permission/all",
    response_model=List[RolePermissionsMappingResponse]
)
def get_all_role_permissions_mapping(
    db: Session = Depends(database.get_postgresql_db),
    *,
    current_user: Annotated[
        TblUsers,
        Security(
            auth_service.get_current_active_user,
            scopes=[security_constants.PERMISSION_READ_ALL_PERMISSIONS_MAPPING]
        )
    ]
)->List[RolePermissionsMappingResponse]:
    """
    API to Get All Role-Permissions Mapping
    :param db:
    :param current_user:
    :return:
    """
    return permission_service.get_all_role_permissions_map(db=db)

@permissions_controller.get(
    "/role_permission/role",
    response_model=RolePermissionsMappingResponse
)
def get_role_permissions_mapping_by_role_id(
    db: Session = Depends(database.get_postgresql_db),
    *,
    id: int,
    current_user: Annotated[
        TblUsers,
        Security(
            auth_service.get_current_active_user,
            scopes=[security_constants.PERMISSION_READ_ROLE_PERMISSIONS_MAPPING_DTL]
        )
    ]
)->RolePermissionsMappingResponse:
    """
    API to Get Role-Permissions Mapping by Role ID
    :param db:
    :param id:
    :param current_user:
    :return:
    """
    return permission_service.get_role_permissions_map(db=db, role_id=id)

@permissions_controller.get(
    "/role_permission/user",
    response_model=UserRolePermissionsMappingsResponse
)
def get_role_permissions_mapping_by_user_id(
    db: Session = Depends(database.get_postgresql_db),
    *,
    id: int,
    current_user: Annotated[
        TblUsers,
        Security(
            auth_service.get_current_active_user,
            scopes=[security_constants.PERMISSION_READ_USER_PERMISSIONS_MAPPING_DTL]
        )
    ]
)->UserRolePermissionsMappingsResponse:
    """
    API to get Role-Permissions Mapping by User ID
    :param db:
    :param id:
    :param current_user:
    :return:
    """
    return permission_service.get_role_permissions_by_user_id(db=db, user_id=id)

@permissions_controller.post("/role_permission/map", response_model=RolePermissionsMappingResponse)
def role_permissions_mapping(
    db: Session = Depends(database.get_postgresql_db),
    *,
    data: RolePermissionsMappingRequest,
    current_user: Annotated[
        TblUsers,
        Security(
            auth_service.get_current_active_user,
            scopes=[security_constants.PERMISSION_WRITE_ROLE_PERMISSIONS_MAPPING]
        )
    ]
)->RolePermissionsMappingResponse:
    """
    API to Plot role_id into permissions
    :param db:
    :param data:
    :param current_user:
    :return:
    """
    return permission_service.role_permission_map(
        db=db,
        role_id=data.role_id,
        mapped_permissions=data.permission_ids
    )

@permissions_controller.delete(
    "/role_permission/map",
    response_model=RolePermissionsMappingResponse
)
def delete_role_permissions_mapping_by_role_id(
    db: Session = Depends(database.get_postgresql_db),
    *,
    role_id: int,
    current_user: Annotated[
        TblUsers,
        Security(
            auth_service.get_current_active_user,
            scopes=[security_constants.PERMISSION_DELETE_ROLE_PERMISSIONS_MAPPING]
        )
    ]
)->RolePermissionsMappingResponse:
    """
    API to Delete Role-Permissions Mapping by role_id
    :param db:
    :param role_id:
    :param current_user:
    :return:
    """
    return permission_service.delete_role_permissions_map_by_role_id(db=db, role_id=role_id)
