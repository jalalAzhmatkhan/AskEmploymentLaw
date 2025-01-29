import json
from typing import List, Optional

from sqlalchemy.orm import Session

from models import TblPermissions, TblRoles, TblRolePermissions, TblUsers, TblUserRole
from schemas import UserRoleSchema, UserRoleNameSchema, UserRolesPermissionsSchema

class CRUDUserRoles:
    """
    CRUD for Tbl_User_Role
    """
    def get_by_id(self, db: Session, id: int) -> Optional[TblUserRole]:
        """
        Get TblUserRole by id
        :param db:
        :param id:
        :return:
        """
        return db.query(TblUserRole).filter(TblUserRole.id == id).first()  # type: ignore

    def get_by_user_id(self, db: Session, user_id: int)->List[TblUserRole]:
        """
        Get TblUserRole by user_id
        :param db:
        :param user_id:
        :return:
        """
        return db.query(TblUserRole).filter(TblUserRole.user_id == user_id).all() # type: ignore

    def get_by_role_id(self, db: Session, role_id: int)->List[TblUserRole]:
        """
        Get TblUserRole by role_id
        :param db:
        :param role_id:
        :return:
        """
        return db.query(TblUserRole).filter(TblUserRole.role_id == role_id).all() # type: ignore

    def get_by_user_id_and_role_id(self, db: Session, user_id: int, role_id: int)->Optional[TblUserRole]:
        """
        Get TblUserRole by user_id and role_id
        :param db:
        :param user_id:
        :param role_id:
        :return:
        """
        return db.query(TblUserRole).filter(
            TblUserRole.user_id == user_id, # type: ignore
            TblUserRole.role_id == role_id, # type: ignore
        ).first()

    def get_user_role_name_by_user_id(
        self,
        db: Session,
        user_id: int
    )->List[UserRoleNameSchema]:
        """
        Get UserRoleName by user_id
        :param db:
        :param user_id:
        :return:
        """
        return db.query(
            TblUserRole.id,
            TblUserRole.user_id,
            TblUserRole.role_id,
            TblUsers.full_name,
            TblRoles.role_name
        ).join(
            TblUsers, TblUsers.id == TblUserRole.user_id, # type: ignore
        ).join(
            TblRoles, TblRoles.id == TblUserRole.role_id, # type: ignore
        ).filter(
            TblUserRole.user_id == user_id # type: ignore
        ).all()

    def get_user_role_permissions_by_user_id(
        self,
        db: Session,
        user_id: int
    )->List[UserRolesPermissionsSchema]:
        """
        Get User's Role, Name, and Permissions by user_id
        :param db:
        :param user_id:
        :return:
        """
        user_roles = db.query(
            TblUserRole.id,
            TblUserRole.role_id,
            TblRoles.role_name,
            TblUsers.full_name,
            TblUserRole.user_id,
        ).join(
            TblUsers, TblUsers.id == TblUserRole.user_id, # type: ignore
        ).join(
            TblRoles, TblRoles.id == TblUserRole.role_id, # type: ignore
        ).filter(
            TblUserRole.user_id == user_id
        ).all() # type: ignore
        responses = []
        for user_role in user_roles:
            permissions = db.query(TblPermissions).distinct().join(
                TblRolePermissions, TblRolePermissions.permission_id == TblPermissions.id,  # type: ignore
            ).filter(
                TblRolePermissions.role_id == user_role.role_id,  # type: ignore
            ).all()
            response = UserRolesPermissionsSchema(
                id=user_role.id,
                user_id=user_id,
                full_name=user_role.full_name,
                role_id=user_role.role_id,
                role_name=user_role.role_name,
                permissions=[permission.permission_name for permission in permissions],
            )
            responses.append(response)
        return responses


    def insert(self, db: Session, obj_in: UserRoleSchema) -> TblUserRole:
        """
        Insert new TblUserRole
        :param db:
        :param obj_in:
        :return:
        """
        db_obj_data = json.loads(obj_in.json())
        db_obj = TblUserRole(**db_obj_data) # type: ignore
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def bulk_insert(self, db: Session, obj_in: List[UserRoleSchema]) -> List[TblUserRole]:
        """
        Insert new TblUserRole
        :param db:
        :param obj_in:
        :return:
        """
        db_obj = [TblUserRole(**json.loads(obj.json())) for obj in obj_in] # type: ignore
        db.add_all(db_obj)
        db.commit()
        for db_obj_data in db_obj:
            db.refresh(db_obj_data)
        return db_obj

    def update(self, db: Session, db_obj: TblUserRole, obj_in: UserRoleSchema) -> TblUserRole:
        """
        Update TblUserRole
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

    def delete(self, db: Session, db_obj: TblUserRole) -> TblUserRole:
        """
        Delete TblUserRole
        :param db:
        :param db_obj:
        :return:
        """
        db.delete(db_obj)
        db.commit()
        return db_obj

crud_tbl_userroles = CRUDUserRoles()
