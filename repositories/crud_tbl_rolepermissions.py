from typing import List, Optional

from sqlalchemy.orm import Session

from models import TblRolePermissions
from schemas import PermissionsUpdateSchema, RolePermissionsScreenSchema

class CRUDTblRolePermissions:
    """
    CRUD for TblRolePermissions
    """
    def get_by_id(self, db: Session, id: int)->Optional[TblRolePermissions]:
        """
        Get TblRolePermissions by id
        :param db:
        :param id:
        :return:
        """
        return db.query(TblRolePermissions).filter(TblRolePermissions.id == id).first() # type: ignore

    def get_by_role_id(self, db: Session, role_id: int)->Optional[TblRolePermissions]:
        """
        Get TblRolePermissions by role_id
        :param db:
        :param role_id:
        :return:
        """
        return db.query(TblRolePermissions).filter(TblRolePermissions.role_id == role_id).first() # type: ignore

    def get_by_permission_id(self, db: Session, permission_id: int)->Optional[TblRolePermissions]:
        """
        Get TblRolePermissions by permission_id
        :param db:
        :param permission_id:
        :return:
        """
        return db.query(TblRolePermissions).filter(TblRolePermissions.permission_id == permission_id).first() # type: ignore

    def get_by_role_permission_id(self, db: Session, role_id: int, permission_id: int)->Optional[TblRolePermissions]:
        """
        Get TblRolePermissions by role_id and permission_id
        :param db:
        :param role_id:
        :param permission_id:
        :return:
        """
        return db.query(TblRolePermissions).filter(
            TblRolePermissions.role_id == role_id,  # type: ignore
            TblRolePermissions.permission_id == permission_id  # type: ignore
        ).first() # type: ignore

    def get_all(self, db: Session)->List[TblRolePermissions]:
        """
        Get all TblRolePermissions
        :param db:
        :return:
        """
        return db.query(TblRolePermissions).all() # type: ignore

    def insert(self, db: Session, obj_in: RolePermissionsScreenSchema) -> TblRolePermissions:
        """
        Insert new TblRolePermissions
        :param db:
        :param obj_in:
        :return:
        """
        db_obj_data = obj_in.model_dump()
        db_obj = TblRolePermissions(**db_obj_data)
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def update(self, db: Session, db_obj: TblRolePermissions,obj_in: PermissionsUpdateSchema) -> TblRolePermissions:
        """
        Update TblRolePermissions
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

    def delete(self, db: Session, db_obj: TblRolePermissions):
        """
        Delete TblRolePermissions
        :param db:
        :param db_obj:
        :return:
        """
        db.delete(db_obj)
        db.commit()
        return db_obj

crud_tbl_rolepermissions = CRUDTblRolePermissions()
