from pydantic import BaseModel

class LoginResponse(BaseModel):
    """
    A class to Declare the Login Response Schema
    """
    access_token: str
    token_type: str
