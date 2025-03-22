import json
from typing import Dict, List, Optional

from sqlalchemy.orm import Session

from models import TblPermissions
from repositories.crud_base import CRUDBase
from schemas import PermissionsSchema, PermissionsUpdateSchema

class CRUDTblPermissions(CRUDBase[TblPermissions, PermissionsSchema, PermissionsUpdateSchema]):
    """
    CRUD for TblPermissions
    """
    def get_by_ids(self, db: Session, ids: List[int])->List[TblPermissions]:
        """
        Get TblPermissions by many ids
        :param db:
        :param ids:
        :return:
        """
        return db.query(TblPermissions).order_by(  # type: ignore
            TblPermissions.permission_name,  # type: ignore
        ).distinct().filter(TblPermissions.id.in_(ids)).all()  # type: ignore

    def get_by_name(self, db: Session, name: str)->Optional[TblPermissions]:
        """
        Get TblPermissions by exact permission name
        :param db:
        :param name:
        :return:
        """
        return db.query(TblPermissions).filter(TblPermissions.permission_name == name).first()  # type: ignore

    def get_all_name_to_dict(self, db: Session)->Dict[str, str]:
        """
        Get TblPermissions by exact permission name to dictionary
        :param db:
        :param name:
        :return:
        """
        db_obj = db.query(TblPermissions).all() # type: ignore
        db_output = {}
        if len(db_obj) > 0:
            for obj in db_obj:
                db_output[obj.permission_name] = obj.permission_description
        return db_output

    def get_by_like_name(self, db: Session, name: str)-> List[TblPermissions]:
        """
        Get TblPermissions by permission name that contains the name
        :param db:
        :param name:
        :return:
        """
        return db.query(TblPermissions).filter(  # type: ignore
            TblPermissions.permission_name.like(f"%{name}%")  # type: ignore
        ).all()  # type: ignore

crud_tbl_permissions = CRUDTblPermissions(TblPermissions)
