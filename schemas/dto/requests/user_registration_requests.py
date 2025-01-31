from pydantic import BaseModel, EmailStr

class UserRegistrationRequest(BaseModel):
    """
    Schema for creating a new user
    """
    full_name: str
    email: EmailStr
    password: str
