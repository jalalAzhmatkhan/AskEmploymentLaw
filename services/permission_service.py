import json
from typing import List

from fastapi import HTTPException
from sqlalchemy.orm import Session

from constants import general as general_constants
from repositories import (
    crud_tbl_permissions,
    crud_tbl_roles,
    crud_tbl_rolepermissions,
    crud_tbl_users,
    crud_tbl_userroles,
)
from schemas import (
    PermissionsResponse,
    PermissionsSchema,
    PermissionsUpdateSchema,
    PermissionsUpdateRequest,
    PermissionsCreateRequest,
    RolePermissionsSchema,
    RolePermissionsMappingResponse,
    UserRolePermissionsMappingsResponse,
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

def get_role_permissions_map(
    db: Session,
    role_id: int,
)->RolePermissionsMappingResponse:
    """
    Function to get Role-Permissions Mapping by role_id
    :param db:
    :param role_id:
    :return:
    """
    found_role = crud_tbl_roles.get_by_id(db=db, id=role_id)
    if not found_role:
        raise HTTPException(
            status_code=general_constants.HTTP_STATUS_ERROR_BAD_REQUEST,
            detail=general_constants.HTTP_STATUS_DETAIL_ROLE_NOT_FOUND,
        )

    found_rolepermission_mappings = crud_tbl_rolepermissions.get_by_role_id(db=db, role_id=role_id)
    mapped_permissions_id = [role_permission.permission_id for role_permission in found_rolepermission_mappings]
    mapped_permissions_id = list(set(mapped_permissions_id))
    mapped_permissions = crud_tbl_permissions.get_by_ids(db=db, ids=mapped_permissions_id)
    permissions = [
        PermissionsResponse(
            id=mapped_permission.id,
            permission_name=mapped_permission.permission_name,
            permission_description=mapped_permission.permission_description
        )
        for mapped_permission in mapped_permissions
    ]
    return RolePermissionsMappingResponse(
        role_id=role_id,
        role_name=found_role.role_name,
        permissions=permissions
    )

def get_all_role_permissions_map(
    db: Session,
)->List[RolePermissionsMappingResponse]:
    """
    Function to get All Role-Permissions Mapping
    :param db:
    :return:
    """
    responses = []
    all_mappings = crud_tbl_rolepermissions.get_all(db=db)
    role_ids = [mapping.role_id for mapping in all_mappings]
    role_ids = list(set(role_ids))
    for role_id in role_ids:
        response = get_role_permissions_map(
            db=db,
            role_id=role_id,
        )
        responses.append(response)
    return responses

def get_role_permissions_by_user_id(
    db: Session,
    user_id: int,
)->UserRolePermissionsMappingsResponse:
    """
    Function to get the user's Role-Permissions mapping
    :param db:
    :param user_id:
    :return:
    """
    found_user = crud_tbl_users.get_by_id(db=db, user_id=user_id)
    if not found_user:
        raise HTTPException(
            status_code=general_constants.HTTP_STATUS_ERROR_BAD_REQUEST,
            detail=general_constants.HTTP_STATUS_DETAIL_USER_NOT_FOUND,
        )
    associated_roles = crud_tbl_userroles.get_by_user_id(db=db, user_id=user_id)
    if len(associated_roles) < 1:
        raise HTTPException(
            status_code=general_constants.HTTP_STATUS_ERROR_BAD_REQUEST,
            detail=general_constants.HTTP_STATUS_DETAIL_NO_ROLES_FOUND,
        )
    assigned_roles_id = [roles.role_id for roles in associated_roles]
    assigned_roles_id = list(set(assigned_roles_id))
    role_permissions = []
    for role_id in assigned_roles_id:
        role_permission = get_role_permissions_map(db=db, role_id=role_id)
        role_permissions.append(role_permission)
    responses = UserRolePermissionsMappingsResponse(
        user_id=user_id,
        full_name=found_user.full_name,
        role_permissions=role_permissions
    )
    return responses

def delete_role_permissions_map_by_role_id(
    db: Session,
    role_id: int
)->RolePermissionsMappingResponse:
    """
    Function to delete all Role-Permissions mapping by its role_id
    :param db:
    :param role_id:
    :return:
    """
    found_role = crud_tbl_roles.get_by_id(db=db, id=role_id)
    if not found_role:
        raise HTTPException(
            status_code=general_constants.HTTP_STATUS_ERROR_BAD_REQUEST,
            detail=general_constants.HTTP_STATUS_DETAIL_ROLE_NOT_FOUND,
        )

    found_rolepermission_mappings = crud_tbl_rolepermissions.get_by_role_id(db=db, role_id=role_id)
    if len(found_rolepermission_mappings) > 0:
        # delete existing role-permissions map
        crud_tbl_rolepermissions.bulk_delete(db=db, db_objs=found_rolepermission_mappings)

    return RolePermissionsMappingResponse(
        role_id=role_id,
        role_name=found_role.role_name,
        permissions=[]
    )

def role_permission_map(
    db: Session,
    role_id: int,
    mapped_permissions: List[int],
)->RolePermissionsMappingResponse:
    """
    Function to map role_id into its permissions
    :param role_id:
    :param db:
    :param mapped_permissions:
    :return:
    """
    found_role = crud_tbl_roles.get_by_id(db=db, id=role_id)
    delete_role_permissions_map_by_role_id(db=db, role_id=role_id)
    inserted_data = [
        RolePermissionsSchema(
            role_id=role_id,
            permission_id=permission,
        )
        for permission in mapped_permissions
    ]
    created_mappings = crud_tbl_rolepermissions.bulk_insert(
        db=db,
        obj_in=inserted_data,
    )
    created_permissions = crud_tbl_permissions.get_by_ids(db=db, ids=mapped_permissions)
    permissions_obj = [
        PermissionsResponse(
            id=created_permission.id,
            permission_name=created_permission.permission_name,
            permission_description=created_permission.permission_description,
        )
        for created_permission in created_permissions
    ]
    response = RolePermissionsMappingResponse(
        role_id=role_id,
        role_name=found_role.role_name,
        permissions=permissions_obj
    )
    return response
