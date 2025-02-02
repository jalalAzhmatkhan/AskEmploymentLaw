from datetime import datetime
from typing import List

from pydantic import BaseModel

class AccessTokenDataSchema(BaseModel):
    """
    Schema for Access Token Data
    """
    exp: int
    sub: str
    role_ids: List[int]
    scopes: List[str] = []
