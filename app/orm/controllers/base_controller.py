from typing import TypeVar, Generic, Type, Optional, Any, Dict, List
from pydantic import BaseModel
from sqlalchemy.exc import SQLAlchemyError
from ..database import db

T = TypeVar("T")
CreateSchemaType = TypeVar("CreateSchemaType", bound=BaseModel)
ReadSchemaType = TypeVar("ReadSchemaType", bound=BaseModel)
UpdateSchemaType = TypeVar("UpdateSchemaType", bound=BaseModel)

class BaseController(Generic[T, CreateSchemaType, ReadSchemaType, UpdateSchemaType]):
    def __init__(self, 
                model: Type[T],
                create_schema: Type[CreateSchemaType],
                read_schema: Type[ReadSchemaType],
                update_schema: Type[UpdateSchemaType]):
        self.model = model
        self.create_schema = create_schema
        self.read_schema = read_schema
        self.update_schema = update_schema

    def _handle_session_errors(func):
        """Decorator para manejar errores de sesión"""
        def wrapper(*args, **kwargs):
            try:
                return func(*args, **kwargs)
            except SQLAlchemyError as e:
                db.session.rollback()
                print(f"⚠️ Database error: {str(e)}")
                raise
            except Exception as e:
                db.session.rollback()
                print(f"⚠️ Unexpected error: {str(e)}")
                raise
        return wrapper

    def get_by_id(self, id: int) -> Optional[ReadSchemaType]:
        """Gets a record by ID and returns it directly as ReadSchema"""
        obj = db.session.query(self.model).get(id)
        return self.read_schema.model_validate(obj) if obj else None

    def get_all(self, filters: Optional[Dict[str, Any]] = None) -> List[ReadSchemaType]:
        """Gets all records already converted to ReadSchemas"""
        query = db.session.query(self.model)
        if filters:
            query = query.filter_by(**filters)
        return [self.read_schema.model_validate(obj) for obj in query.all()]

    @_handle_session_errors
    def create(self, obj_in: CreateSchemaType) -> ReadSchemaType:
        """Creates a new record from a CreateSchema and returns ReadSchema"""
        self._validate_create(obj_in)
        obj_data = obj_in.model_dump()
        db_obj = self.model(**obj_data)
        db.session.add(db_obj)
        db.session.commit()
        db.session.refresh(db_obj)
        return self.read_schema.model_validate(db_obj)

    @_handle_session_errors
    def update(self, id: int, obj_in: UpdateSchemaType | Dict[str, Any]) -> Optional[ReadSchemaType]:
        """Updates a record and returns the updated ReadSchema"""
        db_obj = db.session.query(self.model).get(id)
        if not db_obj:
            return None

        update_data = obj_in.model_dump(exclude_unset=True) if isinstance(obj_in, BaseModel) else obj_in
        for field, value in update_data.items():
            setattr(db_obj, field, value)
            
        db.session.commit()
        db.session.refresh(db_obj)
        return self.read_schema.model_validate(db_obj)

    @_handle_session_errors
    def delete(self, id: int) -> bool:
        """Deletes or disables a record (without schema)"""
        db_obj = db.session.query(self.model).get(id)
        if not db_obj:
            return False

        if hasattr(db_obj, "enable"):
            db_obj.enable = False
            db.session.add(db_obj)
        else:
            db.session.delete(db_obj)
            
        db.session.commit()
        return True

    def _validate_create(self, obj_in: CreateSchemaType):
        """Hook for additional validations when creating"""
        pass