from typing import Optional
from pydantic import BaseModel, EmailStr

class UsersSchema(BaseModel):
    """
    Schema for Tbl_Users
    """
    full_name: str
    email: EmailStr
    hashed_password: str
    is_active: Optional[bool] = False

class UserInDBSchema(UsersSchema):
    """
    Schema for Tbl_Users in DB
    """
    id: int

    class Config:
        """
        Configuration for the ORM mode
        """
        orm_mode = True

class UserUpdateSchema(UsersSchema):
    """
    Schema for updating Tbl_Users
    """
    full_name: Optional[str] = None
    email: Optional[str] = None
    hashed_password: Optional[str] = None
    is_active: Optional[bool] = None
