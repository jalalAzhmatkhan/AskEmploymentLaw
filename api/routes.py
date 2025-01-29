from fastapi import APIRouter

from api.v1 import login_controller

api_router_v1 = APIRouter(prefix="/v1")
api_router_v1.include_router(
    login_controller,
    prefix="/auth",
    tags=["auth"]
)
