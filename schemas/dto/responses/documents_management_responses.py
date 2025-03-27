from datetime import datetime
from typing import Optional

from pydantic import BaseModel

class DocumentUploadResponse(BaseModel):
    """Schema for document upload response"""
    document_name: str
    document_size: int
    document_hash: str
    document_id: int

class AllDocumentsResponse(BaseModel):
    """Schema for all documents response"""
    document_name: str
    document_description: str
    document_type: str
    document_hash: str
    is_uploaded: bool
    uploader_id: int
    uploaded_at: Optional[datetime] = None
    id: int

    class Config:
        """Config for AllDocumentsResponse"""
        from_attributes = True
