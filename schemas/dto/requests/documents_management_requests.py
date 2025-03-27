from pydantic import BaseModel

class DocumentUploadRequest(BaseModel):
    """Schema for document upload request"""
    document_name: str
    document_description: str
    document_type: str

class DocumentDeleteRequest(BaseModel):
    """Schema for document delete request"""
    document_id: int
