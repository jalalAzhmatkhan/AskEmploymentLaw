from pydantic import BaseModel

class DocumentUploadRequest(BaseModel):
    """Schema for document upload request"""
    document_name: str
    document_description: str
    document_type: str
