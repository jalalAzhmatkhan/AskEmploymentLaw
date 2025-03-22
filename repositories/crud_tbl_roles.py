import json
from typing import List, Optional

from sqlalchemy.orm import Session

from models import TblRoles
from repositories.crud_base import CRUDBase
from schemas import RolesSchema

class CRUDTblRoles(CRUDBase[TblRoles, RolesSchema, RolesSchema]):
    """
    CRUD for TblRoles
    """
    def get_by_ids(self, db: Session, ids: List[int])->List[TblRoles]:
        """
        Get TblRoles by many ids
        :param db:
        :param ids:
        :return:
        """
        return db.query(TblRoles).filter(TblRoles.id.in_(ids), # type: ignore
        ).order_by(TblRoles.id).all() # type: ignore

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

    def bulk_insert(self, db: Session, obj_in: List[RolesSchema]) -> List[TblRoles]:
        """
        Insert new TblRoles
        :param db:
        :param obj_in:
        :return:
        """
        db_obj = [TblRoles(**json.loads(db_obj_data.model_dump(mode='json'))) for db_obj_data in obj_in] # type: ignore
        db.add_all(db_obj)
        db.commit()
        for db_obj_data in db_obj:
            db.refresh(db_obj_data)
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

crud_tbl_roles = CRUDTblRoles(TblRoles)
