from typing import List

from fastapi import HTTPException
from sqlalchemy.orm import Session

from constants import general as general_constants
from core.logger import logger
from repositories import (
    crud_tbl_roles,
    crud_tbl_rolepermissions,
    crud_tbl_users,
    crud_tbl_userroles,
)
from schemas import (
    RoleCreate,
    RolesSchema,
    UserRoleSchema,
    RolesScreenResponse,
    RoleUpdate,
    UserRolesMappingRequest,
    UserRolesResponse,
)


def create_new_role(db: Session, data: RoleCreate)->RolesScreenResponse:
    """
    Function to create a new role
    :param db:
    :param data:
    :return:
    """
    if len(data.role_name) < 3:
        raise HTTPException(
            status_code=general_constants.HTTP_STATUS_ERROR_BAD_REQUEST,
            detail=general_constants.HTTP_STATUS_DETAIL_ROLE_NAME_LENGTH_TOO_SHORT,
        )
    created = crud_tbl_roles.insert(
        db=db,
        obj_in=RolesSchema(
            role_name=data.role_name,
        )
    )
    return RolesScreenResponse(
        id=created.id,
        role_name=created.role_name,
    )

def get_all_roles(db: Session)->List[RolesScreenResponse]:
    """
    Function to get All Role names
    :param db:
    :return:
    """
    all_tbl_roles = crud_tbl_roles.get_all(db=db)
    responses = []
    for tbl_roles in all_tbl_roles:
        response = RolesScreenResponse(
            id=tbl_roles.id,
            role_name=tbl_roles.role_name,
        )
        responses.append(response)
    return responses

def get_roles_by_user_id(db: Session, user_id: int)->List[RolesScreenResponse]:
    """
    Function to get All current user's roles
    :param db:
    :param user_id:
    :return:
    """
    roles = []
    try:
        user_roles = crud_tbl_userroles.get_user_role_name_by_user_id(db=db, user_id=user_id)
        if len(user_roles) > 0:
            user_role_ids = [user_role.role_id for user_role in user_roles]
            found_roles = crud_tbl_roles.get_by_ids(db=db, ids=user_role_ids)
            roles = [
                RolesScreenResponse(
                    id=role.id,
                    role_name=role.role_name
                )
                for role in found_roles
            ]
    except Exception as e:
        logger.error(f"get_roles_by_user_id: {e}")
        raise HTTPException(
            status_code=general_constants.HTTP_STATUS_INTERNAL_SERVER_ERROR,
            detail=general_constants.HTTP_STATUS_DETAIL_INTERNAL_SERVER_ERROR
        )
    return roles

def update_role(db: Session, role_id: int, update_data: RoleUpdate)->RolesScreenResponse:
    """
    Function to update role
    :param db:
    :param role_id:
    :param update_data:
    :return:
    """
    found_role = crud_tbl_roles.get_by_id(db=db, id=role_id)
    if not found_role:
        raise HTTPException(
            status_code=general_constants.HTTP_STATUS_ERROR_BAD_REQUEST,
            detail=general_constants.HTTP_STATUS_DETAIL_ROLE_NOT_FOUND,
        )
    updated_role = crud_tbl_roles.update(
        db=db,
        db_obj=found_role,
        obj_in=RolesSchema(
            role_name=update_data.role_name if update_data.role_name else found_role.role_name,
        )
    )
    return RolesScreenResponse(
        id=updated_role.id,
        role_name=updated_role.role_name
    )

def delete_role(db: Session, role_id: int)->RolesScreenResponse:
    """
    Function to delete a role by its id
    :param db:
    :param role_id:
    :return:
    """
    found_role = crud_tbl_roles.get_by_id(db=db, id=role_id)
    found_associated_permissions = crud_tbl_rolepermissions.get_by_role_id(
        db=db,
        role_id=found_role.id,
    )
    if not found_role:
        raise HTTPException(
            status_code=general_constants.HTTP_STATUS_ERROR_BAD_REQUEST,
            detail=general_constants.HTTP_STATUS_DETAIL_ROLE_NOT_FOUND,
        )
    if len(found_associated_permissions) > 0:
        crud_tbl_rolepermissions.bulk_delete(db=db, db_objs=found_associated_permissions)
    deleted_role = crud_tbl_roles.delete(db=db, db_obj=found_role)
    return RolesScreenResponse(
        id=deleted_role.id,
        role_name=deleted_role.role_name,
    )

def get_all_userroles_map(db: Session)->List[UserRolesResponse]:
    """
    Function to get all user-roles mapping
    :param db:
    :return:
    """
    responses = []
    all_users = crud_tbl_users.get_all(db=db)
    for user in all_users:
        response = UserRolesResponse(
            user_id=user.id,
            full_name=user.full_name,
            roles=get_roles_by_user_id(db=db, user_id=user.id)
        )
        responses.append(response)

    return responses

def get_userroles_map_by_user_id(db: Session, user_id: int)->UserRolesResponse:
    """
    Function to get User-Roles mapping by user_id
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
    user_roles = get_roles_by_user_id(db=db, user_id=user_id)
    return UserRolesResponse(
        user_id=user_id,
        full_name=found_user.full_name,
        roles=user_roles,
    )

def user_roles_map(
    db: Session,
    request_data: UserRolesMappingRequest
)->UserRolesResponse:
    """
    Function to map user-roles
    :param db:
    :param request_data:
    :return:
    """
    existing_mapping = crud_tbl_userroles.get_by_user_id(db=db, user_id=request_data.user_id)
    if len(existing_mapping) > 0:
        crud_tbl_userroles.bulk_delete(db=db, db_objs=existing_mapping)

    tobe_inserted_data = [
        UserRoleSchema(
            role_id=role,
            user_id=request_data.user_id,
        )
        for role in request_data.roles_id
    ]
    crud_tbl_userroles.bulk_create(db=db, obj_in=tobe_inserted_data)
    return get_userroles_map_by_user_id(db=db, user_id=request_data.user_id)

def delete_user_roles_map(db: Session, id: int)->UserRolesResponse:
    """
    Function to delete user-roles mapping by id
    :param db:
    :param id:
    :return:
    """
    found_mapping = crud_tbl_userroles.get_by_id(db=db, id=id)
    if not found_mapping:
        raise HTTPException(
            status_code=general_constants.HTTP_STATUS_ERROR_BAD_REQUEST,
            detail=general_constants.HTTP_STATUS_DETAIL_NOT_FOUND,
        )
    found_user = crud_tbl_users.get_by_id(db=db, id=found_mapping.user_id)
    found_role = crud_tbl_roles.get_by_id(db=db, id=found_mapping.role_id)
    crud_tbl_userroles.delete(db=db, db_obj=found_mapping)
    return UserRolesResponse(
        user_id=found_mapping.user_id,
        full_name=found_user.full_name if found_user is not None else "",
        roles=[RolesScreenResponse(
            id=found_role.id,
            role_name=found_role.role_name,
        )]
    )
