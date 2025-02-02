import json
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

    def get_by_ids(self, db: Session, ids: List[int])->Optional[TblPermissions]:
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

    def get_all(self, db:Session)->List[TblPermissions]:
        """
        Get All TblPermissions data
        :param db:
        :return:
        """
        return db.query(TblPermissions).all() # type: ignore

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

    def insert(self, db: Session, obj_in: PermissionsSchema) -> TblPermissions:
        """
        Insert new TblPermissions
        :param db:
        :param obj_in:
        :return:
        """
        db_obj_data = json.loads(obj_in.json())
        db_obj = TblPermissions(**db_obj_data) # type: ignore
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def bulk_insert(
        self,
        db: Session,
        obj_in: List[PermissionsSchema],
    ) -> List[TblPermissions]:
        """
        Insert new TblPermissions
        :param db:
        :param obj_in:
        :return:
        """
        db_obj = [TblPermissions(**json.loads(db_obj_data.json())) for db_obj_data in obj_in] # type: ignore
        db.add_all(db_obj)
        db.commit()
        for db_obj_data in db_obj:
            db.refresh(db_obj_data)
        return db_obj

    def update(self, db: Session, db_obj: TblPermissions, obj_in: PermissionsUpdateSchema) -> TblPermissions:
        """
        Update TblPermissions
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

    def delete(self, db: Session, db_obj: TblPermissions)->TblPermissions:
        """
        Delete TblPermissions
        :param db:
        :param db_obj:
        :return:
        """
        db.delete(db_obj)
        db.commit()
        return db_obj

crud_tbl_permissions = CRUDTblPermissions()
