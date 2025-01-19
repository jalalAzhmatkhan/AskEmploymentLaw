from sqlalchemy import Column, ForeignKey, Integer, LargeBinary
from sqlalchemy.orm import relationship

from models import Base
from models.tbl_documents import TblDocuments

class TblFileStorage(Base):
    """
    Tbl_File_Storage to save uploaded file binaries
    """
    id = Column(Integer, primary_key=True, index=True, nullable=False)
    document_id = Column(Integer, ForeignKey(TblDocuments.id), index=True, nullable=False)
    document_file = Column(LargeBinary)
    documents = relationship("TblDocuments", back_populates="file_storage")
