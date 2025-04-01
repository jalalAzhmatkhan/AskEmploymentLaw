from celery_app import celery_application
from core.logger import logger
from core.utilities import base64_to_bytes
from services import document_management_service
from services.rag.chunking import Chunking

@celery_application.task(
    acks_late=True,
    bind=True,
    name="document_extraction_service.get_dense_vector_from_text"
)
def pdf_document_extraction(
    base64_document: str
):
    """
    Function to extract information from PDF doc
    :return:
    """
    the_document = base64_to_bytes(base64_document)
    # Extract the text
    extracted_text = document_management_service.pdf_extractor(the_document)
    # Chunk it into a smaller parts
    chunker = Chunking(extracted_text)
    text_chunks = chunker.recursive_chunking(
        chunk_size=1000,
        chunk_overlap=200,
    )
    logger.info(f"Number of text chunks: {len(text_chunks)}")
    logger.info(f"Text chunks: {text_chunks}")
