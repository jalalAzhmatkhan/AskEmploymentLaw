from typing import List, Optional

from pydantic import BaseModel

class RoleCreate(BaseModel):
    """
    A schema to create a new Role
    """
    role_name: str

class RoleUpdate(RoleCreate):
    """
    A schema to update a role
    """
    role_name: Optional[str] = None

class UserRolesMappingRequest(BaseModel):
    """
    A schema to map user-roles
    """
    user_id: int
    roles_id: List[int]
