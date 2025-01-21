from pydantic import BaseModel

class DocumentTypeSchema(BaseModel):
    """
    Schema for Tbl_Document_Type model
    """
    document_type: str
    document_extention: str
