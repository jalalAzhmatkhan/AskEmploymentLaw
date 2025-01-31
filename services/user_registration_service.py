from fastapi import HTTPException
from sqlalchemy.orm import Session

from constants import general as general_constants
from core.configs import settings
from core.security import hash_password
from models import TblUsers
from repositories import crud_tbl_users
from schemas import UserRegistrationRequest, UsersSchema, UserUpdateSchema

def create_new_user(db: Session, obj_req: UserRegistrationRequest)->TblUsers:
    """
    Function to create a new user. By default the user is inactive.
    :param db:
    :param obj_req:
    :return:
    """
    existing_user = crud_tbl_users.get_by_email(db=db, email=obj_req.email)
    if existing_user:
        raise HTTPException(
            status_code=general_constants.HTTP_STATUS_ERROR_BAD_REQUEST,
            detail=general_constants.HTTP_STATUS_DETAIL_USER_ALREADY_EXISTS,
        )
    obj_in = UsersSchema(
        full_name=obj_req.full_name,
        email=obj_req.email,
        hashed_password=hash_password(obj_req.password),
    )
    if settings.ENABLE_SEND_EMAIL:
        # Set is_active to be false for the first time
        # allowing it to be activated from the confirmation email
        obj_in.is_active = False
    else:
        # else, automatically set the newly created account as activated
        obj_in.is_active = True
    return crud_tbl_users.insert(db=db, obj_in=obj_in)

def soft_delete_user(db: Session, deleted_user_id: int)->TblUsers:
    """
    Function to softly delete a user based on the user's id
    :param db:
    :param deleted_user_id:
    :return:
    """
    tobe_deleted_user = crud_tbl_users.get_by_id(db=db, id=deleted_user_id)
    if not tobe_deleted_user:
        raise HTTPException(
            status_code=general_constants.HTTP_STATUS_ERROR_BAD_REQUEST,
            detail=general_constants.HTTP_STATUS_DETAIL_USER_ALREADY_DELETED,
        )
    updated_schema = UserUpdateSchema(
        is_active=False
    )
    return crud_tbl_users.update(db=db, db_obj=tobe_deleted_user, obj_in=updated_schema)
