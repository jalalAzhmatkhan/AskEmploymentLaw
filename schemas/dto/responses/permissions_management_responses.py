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
        orm_mode = True
