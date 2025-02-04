from typing import List, Optional

from pydantic import BaseModel

class PermissionsCreateRequest(BaseModel):
    """
    A schema for creating a new Permission
    """
    permission_name: str
    permission_description: str

class PermissionsUpdateRequest(BaseModel):
    """
    Schema for updating a created Permission
    """
    permission_name: Optional[str] = None
    permission_description: Optional[str] = None

class RolePermissionsMappingRequest(BaseModel):
    """
    Schema for mapping a role-permissions
    """
    role_id: int
    permission_ids: List[int]
