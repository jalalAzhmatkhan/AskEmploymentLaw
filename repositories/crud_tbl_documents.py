from datetime import datetime
from typing import List, Optional

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

    def get_all_limited(self, db: Session, limit: int, page: int)->List[TblDocuments]:
        """
        Get all documents with limit and pagination
        :param db:
        :param limit:
        :param page:
        :return:
        """
        return db.query(self.model).limit(limit).offset((page - 1) * limit).all()  # type: ignore

    def get_all_by_uploader_id(self, db: Session, uploader_id: int)->List[TblDocuments]:
        """
        Get all documents by uploader_id
        :param db:
        :param uploader_id:
        :return:
        """
        return db.query(self.model).filter(self.model.uploader_id == uploader_id).all()  # type: ignore

    def get_all_limited_by_uploader_id(
        self,
        db: Session,
        uploader_id: int,
        limit: int,
        page: int
    )->List[TblDocuments]:
        """
        Get all documents by uploader_id with limit and pagination
        :param db:
        :param uploader_id:
        :param limit:
        :param page:
        :return:
        """
        return db.query(self.model).filter(  # type: ignore
            self.model.uploader_id == uploader_id
        ).limit(limit).offset((page - 1) * limit).all()  # type: ignore

    def get_by_like_document_name(self, db: Session, document_name: str)->List[TblDocuments]:
        """
        Get documents by like document_name
        :param db:
        :param document_name:
        :return:
        """
        return db.query(self.model).filter(self.model.document_name.like(f'%{document_name}%')).all()  # type: ignore

    def delete_by_id(self, db: Session, document_id: int)->Optional[TblDocuments]:
        """
        Delete a document by document_id
        :param db:
        :param document_id:
        :return:
        """
        response = db.query(self.model).filter(self.model.id == document_id).first()
        if response:
            db.delete(response)
            db.commit()
            return response  # type: ignore

    def bulk_delete(self, db: Session, document_ids: List[int])->List[TblDocuments]:
        """
        Bulk delete documents by document_ids
        :param db:
        :param document_ids:
        """
        response = db.query(self.model).filter(self.model.id.in_(document_ids)).all()
        db.query(self.model).filter(self.model.id.in_(document_ids)).delete(synchronize_session=False)
        return response  # type: ignore

crud_tbl_documents = CRUDDocuments(TblDocuments)
