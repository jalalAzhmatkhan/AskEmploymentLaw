from typing import Any, Annotated

from fastapi import APIRouter, Depends, Form, HTTPException
from sqlalchemy.orm import Session

from core.db_connection import database
from schemas.dto import responses
from schemas import UserRegistrationRequest
from services import user_registration_service

user_registration_controller = APIRouter()

@user_registration_controller.post(
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
