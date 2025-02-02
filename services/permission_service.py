import json
from typing import List

from fastapi import HTTPException
from sqlalchemy.orm import Session

from constants import general as general_constants
from repositories import crud_tbl_permissions, crud_tbl_userroles, crud_tbl_rolepermissions
from schemas import (
    PermissionsResponse,
    PermissionsSchema,
    PermissionsUpdateSchema,
    PermissionsUpdateRequest,
    PermissionsCreateRequest,
)

def create_a_permission(db: Session, data: PermissionsCreateRequest)->PermissionsResponse:
    """
    A function to create a permission
    :param db:
    :param data:
    :return:
    """
    created_permission = crud_tbl_permissions.insert(
        db=db,
        obj_in=PermissionsSchema(
            permission_name=data.permission_name,
            permission_description=data.permission_description,
        )
    )
    return PermissionsResponse(
        id=created_permission.id,
        permission_name=created_permission.permission_name,
        permission_description=created_permission.permission_description,
    )

def get_all_permissions(db: Session)->List[PermissionsResponse]:
    """
    A function returning all permissions
    :param db:
    :return:
    """
    all_permissions = crud_tbl_permissions.get_all(db=db)
    responses = []
    for permission in all_permissions:
        response = PermissionsResponse(
            id=permission.id,
            permission_name=permission.permission_name,
            permission_description=permission.permission_description,
        )
        responses.append(response)

    return responses

def get_user_permissions(db: Session, user_id: int)->List[PermissionsResponse]:
    """
    A function returning all permissions
    :param user_id:
    :param db:
    :return:
    """
    user_roles = crud_tbl_userroles.get_by_user_id(db=db, user_id=user_id)
    if len(user_roles) < 1:
        raise HTTPException(
            status_code=general_constants.HTTP_STATUS_ERROR_BAD_REQUEST,
            detail=general_constants.HTTP_STATUS_DETAIL_NO_ROLES_FOUND,
        )
    role_permissions_mapping = crud_tbl_rolepermissions.get_by_role_ids(
        db=db,
        role_id=[user_role.role_id for user_role in user_roles]
    )
    permission_ids = [role_permission_mapping.permission_id for role_permission_mapping in role_permissions_mapping]
    permission_ids = list(set(permission_ids))
    all_permissions = crud_tbl_permissions.get_by_ids(db=db, ids=permission_ids)
    responses = []
    for permission in all_permissions:
        response = PermissionsResponse(
            id=permission.id,
            permission_name=permission.permission_name,
            permission_description=permission.permission_description,
        )
        responses.append(response)

    return responses

def update_a_permission(
    db: Session,
    permission_id: int,
    data: PermissionsUpdateRequest
)->PermissionsResponse:
    """
    A function to update a specific permission
    :param db:
    :param permission_id:
    :param data:
    :return:
    """
    found_permission = crud_tbl_permissions.get_by_id(db=db, id=permission_id)
    if not found_permission:
        raise HTTPException(
            status_code=general_constants.HTTP_STATUS_ERROR_BAD_REQUEST,
            detail=general_constants.HTTP_STATUS_DETAIL_PERMISSION_NOT_FOUND,
        )
    updated_data = PermissionsUpdateSchema(**json.loads(data.json()))
    updated_permission = crud_tbl_permissions.update(
        db=db,
        db_obj=found_permission,
        obj_in=updated_data
    )
    return PermissionsResponse(
        id=updated_permission.id,
        permission_name=updated_permission.permission_name,
        permission_description=updated_permission.permission_description,
    )

def delete_a_permission(
    db: Session,
    permission_id: int
)->PermissionsResponse:
    """
    A function to delete a permission by its id
    :param db:
    :param permission_id:
    :return:
    """
    found_permission = crud_tbl_permissions.get_by_id(db=db, id=permission_id)
    if not found_permission:
        raise HTTPException(
            status_code=general_constants.HTTP_STATUS_ERROR_BAD_REQUEST,
            detail=general_constants.HTTP_STATUS_DETAIL_PERMISSION_NOT_FOUND,
        )
    role_permissions = crud_tbl_rolepermissions.get_by_permission_id(db=db, permission_id=permission_id)
    deleted_role_permissions = crud_tbl_rolepermissions.bulk_delete(db=db, db_objs=role_permissions)
    deleted_data = crud_tbl_permissions.delete(db=db, db_obj=found_permission)
    return PermissionsResponse(
        id=deleted_data.id,
        permission_name=deleted_data.permission_name,
        permission_description=deleted_data.permission_description,
    )
