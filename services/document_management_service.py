from datetime import datetime

from sqlalchemy.orm import Session

from models import TblDocuments
from repositories import crud_tbl_documents
from schemas import DocumentsSchema

class DocumentManagementService:
    """
    CRUD Service class for Document Management
    """
    def upload_source_document(
        self,
        db: Session,
        document_name: str,
        document_description: str,
        document_type: str,
        document_hash: str,
        uploader_id: int,
        the_document: bytes,
    )->TblDocuments:
        """
        Function to upload a source document
        :param the_document:
        :param uploader_id:
        :param document_hash:
        :param document_type:
        :param document_description:
        :param document_name:
        :param db:
        :return:
        """
        # Insert the document to the database
        inserted_document = DocumentsSchema(
            document_name=document_name,
            document_description=document_description,
            document_type=document_type,
            document_hash=document_hash,
            is_uploaded=True,
            uploader_id=uploader_id,
            uploaded_at=datetime.now(),
            the_document=the_document
        )
        return crud_tbl_documents.create(db, inserted_document)

document_management_service = DocumentManagementService()
