from datetime import datetime
from typing import List

from sqlalchemy.orm import Session

from models import TblDocuments
from repositories.crud_base import CRUDBase
from schemas import DocumentsSchema, DocumentsUpdateSchema

class CRUDDocuments(CRUDBase[TblDocuments, DocumentsSchema, DocumentsUpdateSchema]):
    """
    CRUD for TblDocuments
    """
    def create(self, db: Session, obj_in: DocumentsSchema)->TblDocuments:
        """
        Create a document
        :param db:
        :param obj_in:
        :return:
        """
        db_obj = TblDocuments(
            document_name=obj_in.document_name,
            document_description=obj_in.document_description,
            document_type=obj_in.document_type,
            document_hash=obj_in.document_hash,
            is_uploaded=obj_in.is_uploaded,
            uploader_id=obj_in.uploader_id,
            uploaded_at=datetime.now(),
            the_document=obj_in.the_document,
        )
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def get_by_like_document_name(self, db: Session, document_name: str)->List[TblDocuments]:
        """
        Get documents by like document_name
        :param db:
        :param document_name:
        :return:
        """
        return db.query(self.model).filter(self.model.document_name.like(f'%{document_name}%')).all()  # type: ignore

crud_tbl_documents = CRUDDocuments(TblDocuments)
