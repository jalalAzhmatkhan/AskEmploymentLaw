from typing import Literal, Optional

from pydantic import BaseModel

class LLMAdapterMessageRequest(BaseModel):
    """
    Schema for LLM Adapter's universal message request
    """
    role: Literal["system", "user"] = "system"
    content: str

class LLMAdapterUserMessageRequest(BaseModel):
    """
    Schema for LLM Adapter's universal message request
    """
    role: Literal["user"] = "user"
    content: str

class LLMAdapterResponse(BaseModel):
    """
    Schema for LLM Adapter's universal message response
    """
    content: str
