from typing import List, Optional

from sqlalchemy.orm import Session

from models import TblUsers
from repositories.crud_base import CRUDBase
from schemas import UsersSchema, UserUpdateSchema

class CRUDTblUsers(CRUDBase[TblUsers, UsersSchema, UserUpdateSchema]):
    """
    CRUD for TblUsers
    """
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

crud_tbl_users = CRUDTblUsers(TblUsers)
