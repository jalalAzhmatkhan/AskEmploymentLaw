import json
from typing import List, Optional

from sqlalchemy.orm import Session

from models import TblPermissions, TblRolePermissions
from repositories.crud_tbl_roles import crud_tbl_roles
from schemas import RolePermissionsSchema, PermissionsUpdateSchema, RolePermissionsScreenSchema

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

    def get_by_role_id(self, db: Session, role_id: int)->List[TblRolePermissions]:
        """
        Get TblRolePermissions by role_id
        :param db:
        :param role_id:
        :return:
        """
        return (db.query(TblRolePermissions).distinct()
                .filter(TblRolePermissions.role_id == role_id).all()) # type: ignore

    def get_permissions_by_role_ids(self, db: Session, role_ids: List[int])->List[RolePermissionsScreenSchema]:
        """
        Get Permission Names by many Role ID
        :param role_ids:
        :return:
        """
        responses = []
        for role_id in role_ids:
            found_role = crud_tbl_roles.get_by_id(db=db, id=role_id)
            permission_ids = db.query(
                TblRolePermissions.permission_id
            ).filter(
                TblRolePermissions.role_id == role_id # type: ignore
            ).all()
            permissions = db.query(TblPermissions.permission_name).filter(
                TblPermissions.id.in_(permission_ids), # type: ignore
            ).all()
            response = RolePermissionsScreenSchema(
                role_name=found_role.role_name if found_role else "",
                permission_names=permissions
            )
        return responses

    def get_by_permission_id(self, db: Session, permission_id: int)->List[TblRolePermissions]:
        """
        Get TblRolePermissions by permission_id
        :param db:
        :param permission_id:
        :return:
        """
        return db.query(TblRolePermissions).distinct().filter(TblRolePermissions.permission_id == permission_id).all() # type: ignore

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

    def insert(self, db: Session, obj_in: RolePermissionsSchema) -> TblRolePermissions:
        """
        Insert new TblRolePermissions
        :param db:
        :param obj_in:
        :return:
        """
        db_obj_data = json.loads(obj_in.json())
        db_obj = TblRolePermissions(**db_obj_data) # type: ignore
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def bulk_insert(self, db: Session, obj_in: List[RolePermissionsSchema]) -> List[TblRolePermissions]:
        """
        Insert new TblRolePermissions
        :param db:
        :param obj_in:
        :return:
        """
        db_obj_data = [TblRolePermissions(**json.loads(obj_in_model.json())) for obj_in_model in obj_in] # type: ignore
        db.add_all(db_obj_data)
        db.commit()
        for db_obj in db_obj_data:
            db.refresh(db_obj)
        return db_obj_data

    def update(self, db: Session, db_obj: TblRolePermissions,obj_in: PermissionsUpdateSchema) -> TblRolePermissions:
        """
        Update TblRolePermissions
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
