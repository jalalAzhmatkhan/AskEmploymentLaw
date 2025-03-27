import json
from typing import Annotated, List

from fastapi import APIRouter, Depends, Form, HTTPException, Security, UploadFile

from sqlalchemy.orm import Session

from constants.core import security as security_constants
from constants.controller import documents_management as documents_management_constants
from constants import general as general_constants
from core.db_connection import database
from core.utilities import hash_a_file
from models import TblUsers
from schemas import (
    AllDocumentsResponse,
    DocumentsInDB,
    DocumentUploadRequest,
    DocumentUploadResponse,
)
from services import document_management_service, get_current_active_user

documents_uploader_controller = APIRouter()

@documents_uploader_controller.get("/documents", response_model=List[AllDocumentsResponse])
def get_all_documents(
    db: Session = Depends(database.get_postgresql_db),
    *,
    limit: int = 10,
    page: int = 1,
    current_user: Annotated[
        TblUsers,
        Security(
            get_current_active_user,
            scopes=[security_constants.PERMISSION_READ_DOCUMENTS]
        )
    ],
) -> List[AllDocumentsResponse]:
    """
    Get all documents
    :param db:
    :param limit:
    :param page:
    :param current_user:
    :return:
    """
    return document_management_service.get_all_documents(db=db, limit=limit, page=page)

@documents_uploader_controller.get("/documents/me", response_model=List[AllDocumentsResponse])
def get_my_uploaded_documents(
    db: Session = Depends(database.get_postgresql_db),
    *,
    limit: int = 10,
    page: int = 1,
    current_user: Annotated[
        TblUsers,
        Security(
            get_current_active_user,
            scopes=[security_constants.PERMISSION_READ_DOCUMENTS]
        )
    ],
) -> List[AllDocumentsResponse]:
    """
    Get all documents uploaded by the current user
    :param db:
    :param limit:
    :param page:
    :param current_user:
    :return:
    """
    return document_management_service.get_uploaded_documents_by_uploader(
        db=db,
        limit=limit,
        page=page,
        uploader_id=current_user.id
    )

@documents_uploader_controller.post("/upload", response_model=DocumentUploadResponse)
async def upload_a_document(
    db: Session = Depends(database.get_postgresql_db),
    *,
    supporting_data: str = Form(...),
    document: UploadFile,
    current_user: Annotated[
        TblUsers,
        Security(
            get_current_active_user,
            scopes=[security_constants.PERMISSION_WRITE_DOCUMENTS]
        )
    ],
):
    """
    Upload a document
    :param db:
    :param current_user:
    :param supporting_data:
    :param document:
    :return:
    """
    if "document_name" not in supporting_data:
        raise HTTPException(
            general_constants.HTTP_STATUS_ERROR_BAD_REQUEST,
            documents_management_constants.ERR_NO_DOCUMENT_NAME
        )
    if "document_description" not in supporting_data:
        raise HTTPException(
            general_constants.HTTP_STATUS_ERROR_BAD_REQUEST,
            documents_management_constants.ERR_NO_DOCUMENT_DESC
        )
    if "document_type" not in supporting_data:
        raise HTTPException(
            general_constants.HTTP_STATUS_ERROR_BAD_REQUEST,
            documents_management_constants.ERR_NO_DOCUMENT_TYPE
        )
    try:
        json.loads(supporting_data)
    except json.JSONDecodeError:
        raise HTTPException(
            general_constants.HTTP_STATUS_ERROR_BAD_REQUEST,
            documents_management_constants.ERR_INVALID_JSON
        )

    document_hash = hash_a_file(document.file)
    parsed_supporting_data = json.loads(supporting_data)
    supporting_data_model = DocumentUploadRequest(**parsed_supporting_data)
    document_contents = await document.read()
    uploaded_document = document_management_service.upload_source_document(
        db=db,
        document_name=supporting_data_model.document_name,
        document_type=supporting_data_model.document_type,
        document_description=supporting_data_model.document_description,
        document_hash=document_hash,
        the_document=document_contents,
        uploader_id=current_user.id,
    )

    return DocumentUploadResponse(
        document_name=document.filename,
        document_size=document.file.__sizeof__(),
        document_hash=document_hash,
        document_id=uploaded_document.id,
    )
