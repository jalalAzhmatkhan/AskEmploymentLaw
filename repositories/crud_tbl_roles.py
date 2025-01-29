import json
from typing import List, Optional

from sqlalchemy.orm import Session

from models import TblRoles
from schemas import RolesSchema

class CRUDTblRoles:
    """
    CRUD for TblRoles
    """
    def get_by_id(self, db: Session, id: int)->Optional[TblRoles]:
        """
        Get TblRoles by id
        :param db:
        :param id:
        :return:
        """
        return db.query(TblRoles).filter(TblRoles.id == id).first() # type: ignore

    def get_by_role_name(self, db: Session, role_name: str)->Optional[TblRoles]:
        """
        Get TblRoles by role_name
        :param db:
        :param role_name:
        :return:
        """
        return db.query(TblRoles).filter(TblRoles.role_name == role_name).first() # type: ignore

    def get_by_like_role_name(self, db: Session, role_name: str)-> List[TblRoles]:
        """
        Get TblRoles by role_name that contains the role_name
        :param db:
        :param role_name:
        :return:
        """
        return db.query(TblRoles).filter(TblRoles.role_name.like(f"%{role_name}%")).all() # type: ignore

    def insert(self, db: Session, obj_in: RolesSchema) -> TblRoles:
        """
        Insert new TblRoles
        :param db:
        :param obj_in:
        :return:
        """
        db_obj_data = json.loads(obj_in.json())
        db_obj = TblRoles(**db_obj_data) # type: ignore
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def bulk_insert(self, db: Session, obj_in: List[RolesSchema]) -> List[TblRoles]:
        """
        Insert new TblRoles
        :param db:
        :param obj_in:
        :return:
        """
        db_obj = [TblRoles(**json.loads(db_obj_data.json())) for db_obj_data in obj_in] # type: ignore
        db.add_all(db_obj)
        db.commit()
        for db_obj_data in db_obj:
            db.refresh(db_obj_data)
        return db_obj

    def update(self, db: Session, db_obj: TblRoles, obj_in: RolesSchema) -> TblRoles:
        """
        Update TblRoles
        :param db:
        :param db_obj:
        :param obj_in:
        :return:
        """
        db_obj_data = json.loads(obj_in.json())
        for key, value in db_obj_data.items():
            setattr(db_obj, key, value)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def delete(self, db: Session, db_obj: TblRoles) -> TblRoles:
        """
        Delete TblRoles
        :param db:
        :param db_obj:
        :return:
        """
        db.delete(db_obj)
        db.commit()
        return db_obj

crud_tbl_roles = CRUDTblRoles()
