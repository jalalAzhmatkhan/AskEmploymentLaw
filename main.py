from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware

from api.routes import api_router_v1
from core.configs import settings

main_app = FastAPI(
    openapi_url=f'{settings.API_STR}/openapi.json',
    title=settings.APP_NAME,
)

if settings.BACKEND_CORS_ORIGINS:
    main_app.add_middleware(
        CORSMiddleware, # type: ignore
        allow_origins=[str(origin) for origin in settings.BACKEND_CORS_ORIGINS],
        allow_credentials=True,
        allow_methods=['*'],
        allow_headers=['*'],
    )

main_app.include_router(api_router_v1, prefix=settings.API_STR)
