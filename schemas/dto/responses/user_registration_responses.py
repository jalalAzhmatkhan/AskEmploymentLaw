from typing import Optional

from pydantic import BaseModel, EmailStr

class UserRegistrationResponse(BaseModel):
    """
    A schema for user registration API response
    """
    id: int
    full_name: str
    email: EmailStr
    hashed_password: str
    is_active: Optional[bool] = False

    class Config:
        """
        Configuration for the ORM mode
        """
        orm_mode = True
