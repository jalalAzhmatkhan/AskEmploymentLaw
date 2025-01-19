from sqlalchemy import Column, ForeignKey, Integer
from sqlalchemy.orm import relationship

from models import Base, TblRoles, TblUsers

class TblUserRole(Base):
    """
    Tbl_User_Role to map users and their roles
    """
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey(TblUsers.id.__str__()))
    role_id = Column(Integer, ForeignKey(TblRoles.id.__str__()))
    user = relationship("TblUsers", back_populates="user_role")
    role = relationship("TblRoles", back_populates="user_role")
