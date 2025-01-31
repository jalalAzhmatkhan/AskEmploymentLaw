from typing import Optional

from pydantic import BaseModel

class PermissionsSchema(BaseModel):
    """
    Schema for Tbl_Permissions
    """
    permission_name: str
    permission_description: str

class PermissionsInDBSchema(PermissionsSchema):
    """
    Schema for Tbl_Permissions in database
    """
    id: int

    class Config:
        """
        Configuration for the ORM mode
        """
        orm_mode = True

class PermissionsUpdateSchema(BaseModel):
    """
    Schema for updating Tbl_Permissions
    """
    permission_name: Optional[str] = None
    permission_description: Optional[str] = None
