from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship

from models import Base

class TblPermissions(Base):
    """
    Tbl_Permissions to store all application permissions
    """
    id = Column(Integer, primary_key=True, index=True)
    permission_name = Column(String, index=True, nullable=False)
    permission_description = Column(String, nullable=True)
    role_permissions = relationship("TblRolePermissions", "permissions")
