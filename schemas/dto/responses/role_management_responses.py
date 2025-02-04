from typing import List

from pydantic import BaseModel

class RolesScreenResponse(BaseModel):
    """
    Schema for Role Management screen
    """
    id: int
    role_name: str

    class Config:
        """
        Configuration for the ORM mode
        """
        orm_mode = True

class UserRolesResponse(BaseModel):
    """
    Schema for User-Roles mapping screen
    """
    user_id: int
    full_name: str
    roles: List[RolesScreenResponse]
