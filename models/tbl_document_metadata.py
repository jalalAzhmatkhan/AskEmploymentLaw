from sqlalchemy import Column, Date, ForeignKey, Integer, String
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
    teu = Column(String)
    number = Column(Integer)
    law_doc_type = Column(String)
    law_doc_type_abbr = Column(String)
    year = Column(Integer)
    place_of_confirmation = Column(String)
    date_of_confirmation = Column(Date)
    date_of_enactment = Column(Date)
    effective_date = Column(Date)
    source = Column(String)
    url_source = Column(String)
    document_url_source = Column(String)
    subject = Column(String)
    valid_status = Column(String)
    language = Column(String)
    location = Column(String)
