from fastapi import APIRouter

from api.v1 import (
    login_controller,
    roles_controller,
    user_management_controller,
)

api_router_v1 = APIRouter(prefix="/v1")
api_router_v1.include_router(
    login_controller,
    prefix="/auth",
    tags=["auth"]
)
api_router_v1.include_router(
    roles_controller,
    prefix="/roles",
    tags=["roles"]
)
api_router_v1.include_router(
    user_management_controller,
    prefix="/users_management",
    tags=["users_management"]
)
