from typing import List
from ..database import db
from .base_controller import BaseController
from ..models.category import Category
from ..schemas.category_schema import CategoryCreate, CategoryUpdate, CategoryRead

class CategoryController(BaseController[Category, CategoryCreate, CategoryRead, CategoryUpdate]):
    def __init__(self):
        super().__init__(Category, CategoryCreate, CategoryRead, CategoryUpdate)

    def get_by_name(self, name: str, enabled: bool = True) -> List[CategoryRead]:
        """Get categories by name"""
        objs = (
            db.session.query(self.model)
            .filter(
                self.model.name == name,
                self.model.enable == enabled
            )
            .all()
        )
        return [CategoryRead.model_validate(obj) for obj in objs]

    def get_all_enable(self, enabled: bool = True) -> List[CategoryRead]:
        """Get all categories, optionally filtered by enabled status"""
        query = db.session.query(self.model)
        if enabled is not None:
            query = query.filter(self.model.enable == enabled)
        objs = query.all()
        return [CategoryRead.model_validate(obj) for obj in objs]

    def _validate_create(self, obj_in: CategoryCreate):
        """Validation hook called automatically from BaseController.create()"""
        pass
