from typing import Dict, Generic, List, Optional, Type, TypeVar, Union

from fastapi.encoders import jsonable_encoder
from pydantic import BaseModel
from sqlalchemy.orm import Session

from models import Base

ModelType = TypeVar("ModelType", bound=Base)
CreateSchemaType = TypeVar("CreateSchemaType", bound=BaseModel)
UpdateSchemaType = TypeVar("UpdateSchemaType", bound=BaseModel)

class CRUDBase(Generic[ModelType, CreateSchemaType, UpdateSchemaType]):
    def __init__(self, model: Type[ModelType]):
        """
        Initialize CRUD object with the model
        :param model:
        """
        self.model = model

    def get_all(self, db: Session)->List[ModelType]:
        """
        Get all data from a table
        :param db:
        :return:
        """
        return db.query(self.model).all()

    def get_by_id(self, db: Session, id: int)->Optional[ModelType]:
        """
        Get data by its id from a table
        :param db:
        :param id:
        :return:
        """
        return db.query(self.model).filter(self.model.id == id).first()  # type: ignore

    def create(self, db: Session, obj_in: CreateSchemaType)->ModelType:
        """
        Create a data to a table
        :param db:
        :param obj_in:
        :return:
        """
        obj_in_data = jsonable_encoder(obj_in)
        db_obj = self.model(**obj_in_data)
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def bulk_create(self, db: Session, obj_in: List[CreateSchemaType])->List[ModelType]:
        """
        Create some data to a table
        :param db:
        :param obj_in:
        :return:
        """
        db_obj = [self.model(**obj_in_data.model_dump(mode='json')) for obj_in_data in obj_in]
        db.add_all(db_obj)
        db.commit()
        for db_obj_item in db_obj:
            db.refresh(db_obj_item)
        return db_obj

    def update(
        self,
        db: Session,
        db_obj: ModelType,
        obj_in: Union[UpdateSchemaType, Dict[str, str]]
    )->ModelType:
        """
        Update a data in a table
        :param db:
        :param db_obj:
        :param obj_in:
        :return:
        """
        obj_data = jsonable_encoder(obj_in)
        update_data = None
        if isinstance(obj_in, dict):
            update_data = obj_in
        else:
            update_data = obj_in.model_dump(mode='json')
        for field in obj_data:
            if field in update_data and update_data[field] is not None:
                setattr(db_obj, field, update_data[field])
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def delete_by_id(self, db: Session, id: int)->Optional[ModelType]:
        """
        Delete a data by its id
        :param db:
        :param id:
        :return:
        """
        found_obj = self.get_by_id(db, id)
        if found_obj:
            db.delete(found_obj)
            db.commit()
            return found_obj
