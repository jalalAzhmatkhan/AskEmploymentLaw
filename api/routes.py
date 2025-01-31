from fastapi import APIRouter

from api.v1 import (
    login_controller,
    user_registration_controller,
)

api_router_v1 = APIRouter(prefix="/v1")
api_router_v1.include_router(
    login_controller,
    prefix="/auth",
    tags=["auth"]
)
api_router_v1.include_router(
    user_registration_controller,
    prefix="/users-management",
    tags=["users-management"]
)
