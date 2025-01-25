from sqlalchemy import Column, Date, ForeignKey, Integer, JSON, String
from sqlalchemy.orm import relationship

from models import Base
from models.tbl_documents import TblDocuments

class TblDocumentMetadata(Base):
    """
    Tbl_Document_Metadata to store the uploaded document's metadata
    """
    id = Column(Integer, primary_key=True, index=True, nullable=False)
    document_id = Column(Integer, ForeignKey(TblDocuments.id))
    documents = relationship("TblDocuments", back_populates="document_metadata")
    title = Column(String, nullable=False)
    number = Column(Integer)
    year = Column(Integer, nullable=False)
    about = Column(String)
    place_of_confirmation = Column(String)
    date_of_confirmation = Column(Date)
    date_of_enactment = Column(Date)
    effective_date = Column(Date)
    changed_by_other_law = Column(JSON)
    removing_other_law = Column(JSON)
