from typing import List, Optional
from pydantic import BaseModel

class RolePermissionsSchema(BaseModel):
    """
    Schema for the Tbl_RolePermissions
    """
    role_id: int
    permission_id: int

class RolePermissionsInDBSchema(RolePermissionsSchema):
    """
    Schema for the Tbl_RolePermissions in the database
    """
    id: int

    class Config:
        """
        Configuration for the ORM mode
        """
        orm_mode = True

class RolePermissionsUpdateSchema(BaseModel):
    """
    Schema for updating the Tbl_RolePermissions
    """
    role_id: Optional[int] = None
    permission_id: Optional[int] = None

class RolePermissionsScreenSchema(BaseModel):
    role_name: str
    permission_names: List[str]

class RolePermissionsScreenSchemaInDB(RolePermissionsScreenSchema):
    """
    Schema for the Tbl_RolePermissions in the database plotted for Frontend
    """
    id: int

    class Config:
        """
        Configuration for the ORM mode
        """
        orm_mode = True
