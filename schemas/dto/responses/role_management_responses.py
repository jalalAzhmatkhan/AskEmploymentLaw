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
