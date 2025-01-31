import json
from typing import List, Optional

from sqlalchemy.orm import Session

from models import TblDocumentType
from schemas import DocumentTypeSchema

class CRUDTblDocumentType:
    """
    CRUD for TblDocumentType
    """
    def get_by_id(self, db: Session, id: int)->Optional[TblDocumentType]:
        """
        Get TblDocumentType by id
        :param db:
        :param id:
        :return:
        """
        return db.query(TblDocumentType).filter(TblDocumentType.id == id).first() # type: ignore

    def get_by_type(self, db: Session, name: str)->Optional[TblDocumentType]:
        """
        Get TblDocumentType by exact document type
        :param db:
        :param name:
        :return:
        """
        return db.query(TblDocumentType).filter(TblDocumentType.document_type == name).first() # type: ignore

    def get_by_like_type(self, db: Session, name: str)-> List[TblDocumentType]:
        """
        Get TblDocumentType by document type that contains the type
        :param db:
        :param name:
        :return:
        """
        return db.query(TblDocumentType).filter(TblDocumentType.document_type.like(f"%{name}%")).all() # type: ignore

    def get_all(self, db: Session)->List[TblDocumentType]:
        """
        Get all TblDocumentType data
        :param db:
        :return:
        """
        return db.query(TblDocumentType).all() # type: ignore

    def insert(self, db: Session, obj_in: DocumentTypeSchema) -> TblDocumentType:
        """
        Insert new TblDocumentType
        :param db:
        :param obj_in:
        :return:
        """
        db_obj_data = json.loads(obj_in.json())
        db_obj = TblDocumentType(**db_obj_data) # type: ignore
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def update(self, db: Session, db_obj: TblDocumentType, obj_in: DocumentTypeSchema) -> TblDocumentType:
        """
        Update TblDocumentType
        :param db:
        :param db_obj:
        :param obj_in:
        :return:
        """
        db_obj_data = json.loads(obj_in.json())
        for field in db_obj_data:
            setattr(db_obj, field, db_obj_data[field])
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def delete(self, db: Session, id: int) -> TblDocumentType:
        """
        Delete TblDocumentType
        :param db:
        :param id:
        :return:
        """
        obj = db.query(TblDocumentType).get(id)
        db.delete(obj)
        db.commit()
        return obj

crud_tbl_document_type = CRUDTblDocumentType()
