from pydantic import BaseModel

class DocumentUploadResponse(BaseModel):
    """Schema for document upload response"""
    document_name: str
    document_size: int
    document_hash: str
    document_id: int
