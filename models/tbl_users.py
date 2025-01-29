from sqlalchemy import Boolean, Column, Integer, String
from sqlalchemy.orm import relationship

from models import Base

class TblUsers(Base):
    """
    Tbl_Users to contain users' information
    """
    id = Column(Integer, primary_key=True, index=True)
    full_name = Column(String, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    is_active = Column(Boolean, default=False)
    user_role = relationship("TblUserRole", back_populates="user")
    documents = relationship("TblDocuments", back_populates="user")
