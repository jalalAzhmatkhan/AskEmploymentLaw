from sqlalchemy import Boolean, Column, DateTime, ForeignKey, Integer, LargeBinary, String
from sqlalchemy.orm import relationship

from models import Base
from models.tbl_users import TblUsers

class TblDocuments(Base):
    """
    Tbl_Documents to store uploaded documents
    """
    id = Column(Integer, primary_key=True, index=True, nullable=False)
    document_name = Column(String, nullable=True)
    document_description = Column(String)
    document_type = Column(String, nullable=False)
    uploaded_at = Column(DateTime, index=True, nullable=False)
    is_uploaded = Column(Boolean, index=True)
    uploader_id = Column(Integer, ForeignKey(TblUsers.id), nullable=False)
    the_document = Column(LargeBinary, nullable=True)
    user = relationship("TblUsers", back_populates="documents")
