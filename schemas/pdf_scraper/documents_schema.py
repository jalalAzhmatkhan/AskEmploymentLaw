from datetime import datetime
from pydantic import BaseModel
from typing import Optional

class DocumentsSchema(BaseModel):
    """
    Schema for Tbl_Documents
    """
    document_name: Optional[str] = None
    document_description: Optional[str] = None
    document_type_id: int
    uploaded_at: datetime
    is_uploaded: Optional[bool] = False
    uploader_id: int
