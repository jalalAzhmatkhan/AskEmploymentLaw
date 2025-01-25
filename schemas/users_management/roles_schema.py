from pydantic import BaseModel

class RolesSchema(BaseModel):
    """
    Schema for Tbl_Roles
    """
    role_name: str

class RolesInDBSchema(RolesSchema):
    """
    Schema for Tbl_Roles in DB
    """
    id: int

    class Config:
        orm_mode = True
