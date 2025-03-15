from typing import List, Optional

from pydantic import BaseModel

class UserRoleSchema(BaseModel):
    """
    Schema for Tbl_User_Role
    """
    user_id: int
    role_id: int

class UserRoleInDBSchema(UserRoleSchema):
    """
    Schema for Tbl_User_Role from the database
    """
    id: int

    class Config:
        """
        Configuration schema
        """
        from_attributes = True

class UserRoleUpdateSchema(UserRoleSchema):
    """
    Schema for Updating table Tbl_User_Role
    """
    user_id: Optional[int] = None
    role_id: Optional[int] = None

class UserRoleNameSchema(UserRoleInDBSchema):
    """
    Schema for Displaying the User's Full name and Role(s) Name
    """
    full_name: str
    role_name: str

class UserRolesPermissionsSchema(UserRoleNameSchema):
    """
    Schema for Displaying the User's Full name, Role(s) name, and its Permission(s)
    """
    permissions: List[str]
