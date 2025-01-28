from typing import Dict, List, Optional

from sqlalchemy.orm import Session

from models import TblPermissions
from schemas import PermissionsSchema, PermissionsUpdateSchema

class CRUDTblPermissions:
    """
    CRUD for TblPermissions
    """
    def get_by_id(self, db: Session, id: int)->Optional[TblPermissions]:
        """
        Get TblPermissions by id
        :param db:
        :param id:
        :return:
        """
        return db.query(TblPermissions).filter(TblPermissions.id == id).first() # type: ignore

    def get_by_name(self, db: Session, name: str)->Optional[TblPermissions]:
        """
        Get TblPermissions by exact permission name
        :param db:
        :param name:
        :return:
        """
        return db.query(TblPermissions).filter(TblPermissions.permission_name == name).first() # type: ignore

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
        return db.query(TblPermissions).filter(TblPermissions.permission_name.like(f"%{name}%")).all() # type: ignore

    def insert(self, db: Session, obj_in: PermissionsSchema) -> TblPermissions:
        """
        Insert new TblPermissions
        :param db:
        :param obj_in:
        :return:
        """
        db_obj_data = obj_in.model_dump()
        db_obj = TblPermissions(**db_obj_data) # type: ignore
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def update(self, db: Session, db_obj: TblPermissions, obj_in: PermissionsUpdateSchema) -> TblPermissions:
        """
        Update TblPermissions
        :param db:
        :param db_obj:
        :param obj_in:
        :return:
        """
        db_obj_data = obj_in.model_dump()
        for key, value in db_obj_data.items():
            setattr(db_obj, key, value)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def delete(self, db: Session, db_obj: TblPermissions):
        """
        Delete TblPermissions
        :param db:
        :param db_obj:
        :return:
        """
        db.delete(db_obj)
        db.commit()

crud_tbl_permissions = CRUDTblPermissions()
