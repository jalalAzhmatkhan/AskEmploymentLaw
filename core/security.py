from datetime import datetime, timedelta
import json
from typing import Any, List, Union

from fastapi.security import OAuth2PasswordBearer
from jose import jwt
from passlib.context import CryptContext

from constants.core import security as security_constants
from core.db_connection import database
from core.configs import settings
from repositories.crud_tbl_permissions import crud_tbl_permissions
from schemas.core import security as security_schemas

pwd_context = CryptContext(schemes=[security_constants.BCRYPT_SCHEMA], deprecated="auto")
db = database.SessionLocal()
all_permissions_dict = crud_tbl_permissions.get_all_name_to_dict(db=db)
oauth2_scheme = OAuth2PasswordBearer(
    tokenUrl=settings.AUTHENTICATION_URI,
    scopes=all_permissions_dict,
)

def create_access_token(
    role_id: List[int],
    permissions: List[str],
    subject: Union[str, Any],
    expires_delta: timedelta = None
) -> str:
    """
    Function to create an access token.
    :param role_id:
    :param permissions:
    :param subject:
    :param expires_delta:
    :return:
    """
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(
            minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES
        )
    to_encode = security_schemas.AccessTokenDataSchema(
        exp=expire,
        role_ids=role_id,
        scopes=permissions,
        sub=subject
    )
    encoded_jwt = jwt.encode(
        json.loads(to_encode.json()),
        settings.SECRET_KEY,
        algorithm=security_constants.ENCODING_ALGORITHM
    )
    return encoded_jwt

def hash_password(password: str) -> str:
    """
    Hashes a password using bcrypt.

    :param password: The plaintext password to hash.
    :return: A hashed password as a string.
    """
    if not isinstance(password, str) or not password:
        raise ValueError("Password must be a non-empty string.")

    return pwd_context.hash(password)

def verify_password(plain_password: str, hashed_password: str) -> bool:
    """
    Verifies a password against a hashed password.

    :param plain_password: The plaintext password to verify.
    :param hashed_password: The hashed password to compare with.
    :return: True if the password matches, False otherwise.
    """
    if not isinstance(plain_password, str) or not isinstance(hashed_password, str):
        raise ValueError("verify_password: Both password and hashed_password must be strings.")

    return pwd_context.verify(plain_password, hashed_password)
