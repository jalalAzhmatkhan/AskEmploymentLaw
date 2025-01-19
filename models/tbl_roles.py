from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship

from models import Base

class TblRoles(Base):
    """
    Tbl_Roles to store all application roles
    """
    id = Column(Integer, primary_key=True, index=True)
    role_name = Column(String, index=True)
    role_permissions = relationship("TblRolePermissions", back_populates="role")
    user_role = relationship("TblUserRole", back_populates="role")
