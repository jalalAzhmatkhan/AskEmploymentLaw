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
    number: Optional[int] = None
    year: int
    about: Optional[str] = None
    place_of_confirmation: Optional[str] = None
    date_of_confirmation: Optional[date] = None
    date_of_enactment: Optional[date] = None
    effective_date: Optional[date] = None
    changed_by_other_law: Optional[List[ScrapedLawStatusSchema]] = None
    removing_other_law: Optional[List[ScrapedLawStatusSchema]] = None
