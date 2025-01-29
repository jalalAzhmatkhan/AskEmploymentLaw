import json
from typing import List, Optional

from sqlalchemy.orm import Session

from models import TblUsers
from schemas import UsersSchema

class CRUDTblUsers:
    """
    CRUD for TblUsers
    """
    def get_by_id(self, db: Session, id: int)->Optional[TblUsers]:
        """
        Get TblUsers by id
        :param db:
        :param id:
        :return:
        """
        return db.query(TblUsers).filter(TblUsers.id == id).first() # type: ignore

    def get_by_email(self, db: Session, email: str)->Optional[TblUsers]:
        """
        Get TblUsers by email
        :param db:
        :param email:
        :return:
        """
        return db.query(TblUsers).filter(TblUsers.email == email).first() # type: ignore

    def get_by_like_name(self, db: Session, name: str)-> List[TblUsers]:
        """
        Get TblUsers by username that contains the username
        :param db:
        :param name:
        :return:
        """
        return db.query(TblUsers).filter(TblUsers.full_name.like(f"%{name}%")).all() # type: ignore

    def insert(self, db: Session, obj_in: UsersSchema) -> TblUsers:
        """
        Insert new TblUsers
        :param db:
        :param obj_in:
        :return:
        """
        db_obj_data = json.loads(obj_in.json())
        db_obj = TblUsers(**db_obj_data) # type: ignore
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def update(self, db: Session, db_obj: TblUsers, obj_in: UsersSchema) -> TblUsers:
        """
        Update TblUsers
        :param db:
        :param db_obj:
        :param obj_in:
        :return:
        """
        obj_data = json.loads(obj_in.json())
        for key, value in obj_data.items():
            setattr(db_obj, key, value)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def delete(self, db: Session, id: int):
        """
        Delete TblUsers
        :param db:
        :param id:
        :return:
        """
        db.query(TblUsers).filter(TblUsers.id == id).delete() # type: ignore
        db.commit()
        return True

crud_tbl_users = CRUDTblUsers()
