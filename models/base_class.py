from typing import Any

from sqlalchemy.ext.declarative import as_declarative, declared_attr

from core.utilities import camel_to_snake

@as_declarative()
class Base:
    """
    Base class for all models
    """
    id: Any
    __name__: str
    __table_args__ = { 'extend_existing': True }
    # Generate __tablename__ automatically
    @declared_attr
    def __tablename__(self) -> str:
        return camel_to_snake(self.__name__)
