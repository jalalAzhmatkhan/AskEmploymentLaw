from sqlalchemy import Column, ForeignKey, Integer
from sqlalchemy.orm import relationship

from models import Base
from models.tbl_roles import TblRoles
from models.tbl_permissions import TblPermissions

class TblRolePermissions(Base):
    """
    Tbl_Role_Permissions to store role-permissions relationship
    """
    id = Column(Integer, primary_key=True, index=True)
    permission_id = Column(Integer, ForeignKey(TblPermissions.id))
    role_id = Column(Integer, ForeignKey(TblRoles.id))
    role = relationship("TblRoles", back_populates="role_permissions")
    permissions = relationship("TblPermissions", back_populates="role_permissions")
