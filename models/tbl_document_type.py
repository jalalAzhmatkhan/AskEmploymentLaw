from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship

from models import Base

class TblDocumentType(Base):
    """
    Tbl_Document_Type to save the uploaded document's type
    """
    id = Column(Integer, primary_key=True, index=True)
    document_type = Column(String, index=True)
    document_extention = Column(String, index=True)
    documents = relationship("TblDocuments", back_populates="document_type")
