from datetime import datetime
from typing import List

from pydantic import BaseModel

class AccessTokenDataSchema(BaseModel):
    """
    Schema for Access Token Data
    """
    exp: datetime
    sub: str
    role_id: int
    scopes: List[str] = []
