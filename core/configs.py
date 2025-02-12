import os
from typing import Any, Dict, List, Literal, Optional, Union

from dotenv import load_dotenv
from pydantic import AnyHttpUrl, validator
from pydantic_settings import BaseSettings

dotenv_path = os.path.join(os.path.abspath(os.path.dirname(os.path.dirname(__file__))), ".env")
if not os.path.exists(dotenv_path):
    raise ValueError("No .env file found.")

load_dotenv(dotenv_path)

class Settings(BaseSettings):
    """
    A class to Declare and use Configurations in this App
    """
    # App Config
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60
    AUTHENTICATION_URI: str = "/api/v1/auth/login"
    API_STR: str = "/api"
    APP_NAME: str
    BACKEND_CORS_ORIGINS: Optional[List[AnyHttpUrl]] = None

    @validator("BACKEND_CORS_ORIGINS", pre=True)
    def assemble_cors_origins(cls, v: Union[str, List[str]]) -> Union[List[str], str]:
        if isinstance(v, str) and not v.startswith("["):
            return [i.strip() for i in v.split(",")]
        elif isinstance(v, (list, str)):
            return v
        raise ValueError(v)

    SECRET_KEY: str = None

    # Database config
    DATABASE_HOST: str
    DATABASE_PORT: str
    DATABASE_SCHEMA: Optional[str] = "public"
    DATABASE_USE_CREDENTIALS: Optional[bool] = True
    DATABASE_USERNAME: Optional[str] = None
    DATABASE_PASSWORD: Optional[str] = None
    DATABASE_DEFAULT_DB: Optional[str] = "postgres"
    DATABASE_ENGINE: Literal['postgresql', 'starrocks'] = 'postgresql'
    DATABASE_CONNECTION_MAX_TRIES: int
    DATABASE_CONNECTION_WAIT_SEC: int
    DATABASE_FULL_URI: Optional[str] = None

    @validator("DATABASE_FULL_URI", pre=True)
    def assemble_db_uri(cls, v: Optional[str], values: Dict[str, Any]) -> str:
        """
        Function to Assemble DB connection string URI
        """
        if isinstance(v, str):
            return v

        return (f'{values.get("DATABASE_ENGINE")}://{values.get("DATABASE_USERNAME")}:'
                f'{values.get("DATABASE_PASSWORD") if values.get("DATABASE_USE_CREDENTIALS") else ""}@'
                f'{values.get("DATABASE_HOST")}:{values.get("DATABASE_PORT")}/'
                f'{values.get("DATABASE_DEFAULT_DB") or ""}'
        )

    # Email config
    ENABLE_SEND_EMAIL: bool = False

    # SuperAdmin config
    FIRST_SUPERADMIN_EMAIL: str
    FIRST_SUPERADMIN_NAME: str
    FIRST_SUPERADMIN_PASSWORD: str

    # Logging Directory
    LOG_DIR: str

    # RabbitMQ config
    RABBITMQ_HOST: str
    RABBITMQ_PORT: str
    RABBITMQ_USE_CREDENTIALS: bool
    RABBITMQ_USERNAME: str
    RABBITMQ_PASSWORD: str
    RABBITMQ_CONNECTION_MAX_TRIES: int
    RABBITMQ_WAIT_SECONDS: int

    # Vector Database config
    VECTOR_DB_HOST: str
    VECTOR_DB_PORT: str
    VECTOR_DB_COLLECTION: Optional[str] = None
    VECTOR_DB_USE_CREDENTIALS: Optional[bool] = False
    VECTOR_DB_USERNAME: Optional[str] = None
    VECTOR_DB_PASSWORD: Optional[str] = None
    VECTOR_DB_ENGINE: Literal['milvus'] = 'milvus'
    VECTOR_DB_CONNECTION_MAX_TRIES: int
    VECTOR_DB_CONNECTION_WAIT_SEC: int

    class Config:
        """ Additional config """
        case_sensitive = True

settings = Settings()
