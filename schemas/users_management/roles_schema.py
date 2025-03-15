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
        """
        Configuration for the ORM mode
        """
        from_attributes = True
