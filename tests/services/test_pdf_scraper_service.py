import pytest

from constants.services import pdf_scraper as pdf_scraper_constants
from services.pdf_scraper_service import Scraper

@pytest.mark.asyncio
async def test_pdf_scraper_service():
    """Unit test for pdf scraper service"""
    law_scraper = Scraper(
        url=pdf_scraper_constants.LAW_SCRAPER_STARTING_PAGE,
        llm_service="ollama",
        llm_model="mistral",
        llm_tag="latest",
        llm_host="http://localhost",
        llm_port=11434,
    )
    results = await law_scraper.scrape()


    assert isinstance(results, list), "Wrong data type."
    assert len(results) > 0, "No result"
