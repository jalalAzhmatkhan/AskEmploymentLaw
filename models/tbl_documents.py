from sqlalchemy import Boolean, Column, DateTime, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from models import Base
from models.tbl_document_type import TblDocumentType
from models.tbl_users import TblUsers

class TblDocuments(Base):
    """
    Tbl_Documents to store uploaded documents
    """
    id = Column(Integer, primary_key=True, index=True, nullable=False)
    document_name = Column(String, nullable=True)
    document_description = Column(String)
    document_type_id = Column(Integer, ForeignKey(TblDocumentType.id), index=True, nullable=False)
    uploaded_at = Column(DateTime, index=True, nullable=False)
    is_uploaded = Column(Boolean, index=True)
    uploader_id = Column(Integer, ForeignKey(TblUsers.id), nullable=False)
    document_type = relationship("TblDocumentType", back_populates="documents")
    user = relationship("TblUsers", back_populates="documents")
    document_metadata = relationship("TblDocumentMetadata", back_populates="documents")
