import json
from typing import List, Optional

from sqlalchemy.orm import Session
from sqlalchemy import delete

from models import TblPermissions, TblRolePermissions
from repositories.crud_base import CRUDBase
from repositories.crud_tbl_roles import crud_tbl_roles
from schemas import (
    RolePermissionsSchema,
    RolePermissionsUpdateSchema,
    RolePermissionsScreenSchema
)

class CRUDTblRolePermissions(CRUDBase[TblRolePermissions, RolePermissionsSchema, RolePermissionsUpdateSchema]):
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
        return (db.query(TblRolePermissions).distinct()  # type: ignore
                .filter(TblRolePermissions.role_id == role_id).all())  # type: ignore

    def get_by_role_ids(self, db: Session, role_id: List[int])->List[TblRolePermissions]:
        """
        Get TblRolePermissions by role_id
        :param db:
        :param role_id:
        :return:
        """
        return (db.query(TblRolePermissions).distinct()  # type: ignore
                .filter(
                TblRolePermissions.role_id.in_(role_id),  # type: ignore
        ).all())  # type: ignore

    def get_permissions_by_role_ids(
        self,
        db: Session,
        role_ids: List[int],
    )->List[RolePermissionsScreenSchema]:
        """
        Get Permission Names by many Role ID
        :param db:
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
            responses.append(response)
        return responses

    def get_by_permission_id(self, db: Session, permission_id: int)->List[TblRolePermissions]:
        """
        Get TblRolePermissions by permission_id
        :param db:
        :param permission_id:
        :return:
        """
        return (db.query(TblRolePermissions).distinct()  # type: ignore
                .filter(TblRolePermissions.permission_id == permission_id).all())  # type: ignore

    def get_by_permission_ids(self, db: Session, permission_ids: List[int])->List[TblRolePermissions]:
        """
        Get TblRolePermissions by many permission_id
        :param db:
        :param permission_ids:
        :return:
        """
        return (db.query(TblRolePermissions).distinct().order_by(TblRolePermissions.role_id)  # type: ignore
                .filter(TblRolePermissions.permission_id.in_(permission_ids)).all())  # type: ignore

    def get_by_role_permission_id(
        self,
        db: Session,
        role_id: int,
        permission_id: int,
    )->Optional[TblRolePermissions]:
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
        ).first()  # type: ignore

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

    def delete(self, db: Session, db_obj: TblRolePermissions)->TblRolePermissions:
        """
        Delete TblRolePermissions
        :param db:
        :param db_obj:
        :return:
        """
        db.delete(db_obj)
        db.commit()
        return db_obj

    def bulk_delete(self, db: Session, db_objs: List[TblRolePermissions])->List[TblRolePermissions]:
        """
        Delete rows of TblRolePermissions
        :param db:
        :param db_objs:
        :return:
        """
        if not db_objs:
            return
        role_permission_ids = [role_permission.id for role_permission in db_objs]
        db.execute(
            delete(TblRolePermissions).where(
                TblRolePermissions.id.in_(role_permission_ids) # type: ignore
            )
        )
        db.commit()
        return db_objs

crud_tbl_rolepermissions = CRUDTblRolePermissions(TblRolePermissions)
