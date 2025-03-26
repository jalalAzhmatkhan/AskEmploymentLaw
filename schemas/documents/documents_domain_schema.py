from datetime import datetime
from typing import Optional

from pydantic import BaseModel

class DocumentsSchema(BaseModel):
    """Schema for documents domain."""
    document_name: str
    document_description: str
    document_type: str
    document_hash: str
    is_uploaded: bool
    uploader_id: int
    uploaded_at: Optional[datetime] = None
    the_document: bytes

class DocumentsInDB(DocumentsSchema):
    """Schema for documents domain in database."""
    id: int

    class Config:
        from_attributes = True

class DocumentsUpdateSchema(BaseModel):
    """Schema for updating documents domain."""
    document_name: Optional[str] = None
    document_description: Optional[str] = None
    document_type: Optional[str] = None
    document_hash: Optional[str] = None
    is_uploaded: Optional[bool] = False
    uploader_id: Optional[int] = None
    the_document: Optional[bytes] = None
    uploaded_at: Optional[datetime] = None
