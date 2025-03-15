from typing import List

from pydantic import BaseModel

class PermissionsResponse(BaseModel):
    """
    A schema for Displaying Permissions on the Frontend
    """
    id: int
    permission_name: str
    permission_description: str

    class Config:
        """
        Configuration for the ORM mode
        """
        from_attributes = True

class RolePermissionsMappingResponse(BaseModel):
    """
    A schema for Displaying Role-Permissions mapping Response
    """
    role_id: int
    role_name: str
    permissions: List[PermissionsResponse]

class UserRolePermissionsMappingsResponse(BaseModel):
    """
    A schema for Displaying the User's Role-Permissions mapping Response
    """
    user_id: int
    full_name: str
    role_permissions: List[RolePermissionsMappingResponse]
