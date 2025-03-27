from datetime import datetime
from typing import List

from sqlalchemy.orm import Session

from models import TblDocuments
from repositories import crud_tbl_documents
from schemas import (
    AllDocumentsResponse,
    DocumentsSchema,
    DocumentsInDB,
)

class DocumentManagementService:
    """
    CRUD Service class for Document Management
    """
    def get_all_documents(
        self,
        db: Session,
        limit: int = 10,
        page: int = 1
    )->List[AllDocumentsResponse]:
        """
        Function to get all documents
        :return:
        """
        responses_from_crud = []
        if limit == 0 and page == 0:
            responses_from_crud = crud_tbl_documents.get_all()
        elif limit > 0 and page > 0:
            responses_from_crud = crud_tbl_documents.get_all_limited(db, limit, page)
        responses = [AllDocumentsResponse(
            id=resp.id,
            document_name=resp.document_name,
            document_type=resp.document_type,
            document_description=resp.document_description,
            document_hash=resp.document_hash,
            is_uploaded=resp.is_uploaded,
            uploader_id=resp.uploader_id,
            uploaded_at=resp.uploaded_at,
        ) for resp in responses_from_crud]
        return responses

    def get_uploaded_documents_by_uploader(
        self,
        db: Session,
        uploader_id: int,
        limit: int = 10,
        page: int = 1,
    )->List[AllDocumentsResponse]:
        """
        Function to get all documents uploaded by the current user
        :return:
        """
        responses_from_crud = []
        if limit == 0 and page == 0:
            responses_from_crud = crud_tbl_documents.get_all_by_uploader_id(db, uploader_id)
        elif limit > 0 and page > 0:
            responses_from_crud = crud_tbl_documents.get_all_limited_by_uploader_id(db, uploader_id, limit, page)

        responses = [AllDocumentsResponse(
            id=resp.id,
            document_name=resp.document_name,
            document_type=resp.document_type,
            document_description=resp.document_description,
            document_hash=resp.document_hash,
            is_uploaded=resp.is_uploaded,
            uploader_id=resp.uploader_id,
            uploaded_at=resp.uploaded_at,
        ) for resp in responses_from_crud]

        return responses

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
