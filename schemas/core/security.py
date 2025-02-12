from typing import List, Union

from pydantic import BaseModel

class AccessTokenDataSchema(BaseModel):
    """
    Schema for Access Token Data
    """
    exp: Union[float, int]
    sub: str
    role_ids: List[int]
    scopes: List[str] = []
