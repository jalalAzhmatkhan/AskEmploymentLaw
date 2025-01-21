from datetime import date
from typing import List, Optional

from pydantic import BaseModel

from schemas.pdf_scraper.scraped_law_status_schema import ScrapedLawStatusSchema

class DocumentMetadataSchema(BaseModel):
    """
    Schema for Tbl_Document_Metadata
    """
    document_id: int
    title: str
    teu: Optional[str] = None
    number: Optional[int] = None
    law_doc_type: Optional[str] = None
    law_doc_type_abbr: Optional[str] = None
    year: Optional[int] = None
    place_of_confirmation: Optional[str] = None
    date_of_confirmation: Optional[date] = None
    date_of_enactment: Optional[date] = None
    effective_date: Optional[date] = None
    source: Optional[str] = None
    url_source: Optional[str] = None
    document_url_source: Optional[str] = None
    subject: Optional[str] = None
    valid_status: Optional[str] = None
    language: Optional[str] = None
    location: Optional[str] = None
    changed_by_other_law: Optional[List[ScrapedLawStatusSchema]] = None
    removing_other_law: Optional[List[ScrapedLawStatusSchema]] = None
