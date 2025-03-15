from typing import Optional
from pydantic import BaseModel

class ScrapedLawStatusSchema(BaseModel):
    """
    A schema for scraped Law Status
    """
    title: str
    about: str
    url: Optional[str] = None
