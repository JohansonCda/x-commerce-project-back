from typing import List
from ..database import db
from .base_controller import BaseController
from ..models.product import Product
from ..schemas.product_schema import ProductCreate, ProductUpdate, ProductRead

class ProductController(BaseController[Product, ProductCreate, ProductRead, ProductUpdate]):
    def __init__(self):
        super().__init__(Product, ProductCreate, ProductRead, ProductUpdate)

    def get_by_name(self, name: str, enabled: bool = True) -> List[ProductRead]:
        """Get products by name"""
        objs = (
            db.session.query(self.model)
            .filter(
                self.model.name == name,
                self.model.enable == enabled
            )
            .all()
        )
        return [ProductRead.model_validate(obj) for obj in objs]

    def get_all_enable(self, enabled: bool = True) -> List[ProductRead]:
        """Get all products, optionally filtered by enabled status"""
        query = db.session.query(self.model)
        if enabled is not None:
            query = query.filter(self.model.enable == enabled)
        objs = query.all()
        return [ProductRead.model_validate(obj) for obj in objs]

    def get_by_price_range(self, min_price: float, max_price: float, enabled: bool = True) -> List[ProductRead]:
        """Get products within a price range"""
        objs = (
            db.session.query(self.model)
            .filter(
                self.model.price >= min_price,
                self.model.price <= max_price,
                self.model.enable == enabled
            )
            .all()
        )
        return [ProductRead.model_validate(obj) for obj in objs]

    def get_by_stock(self, min_stock: int = 1, enabled: bool = True) -> List[ProductRead]:
        """Get products with stock greater than or equal to min_stock"""
        objs = (
            db.session.query(self.model)
            .filter(
                self.model.stock >= min_stock,
                self.model.enable == enabled
            )
            .all()
        )
        return [ProductRead.model_validate(obj) for obj in objs]
    
    def get_by_category(self, category_id: int, enabled: bool = True) -> List[ProductRead]:
        """Get products by category id"""
        objs = (
            db.session.query(self.model)
            .filter(
                self.model.category_id == category_id,
                self.model.enable == enabled
            )
            .all()
        )
        return [ProductRead.model_validate(obj) for obj in objs]
    
    def get_by_category_name(self, category_name: str, enabled: bool = True) -> List[ProductRead]:
        """Get products by category name"""
        objs = (
            db.session.query(self.model)
            .join(self.model.category)
            .filter(
                self.model.category.has(name=category_name),
                self.model.enable == enabled
            )
            .all()
        )
        return [ProductRead.model_validate(obj) for obj in objs]

    def _validate_create(self, obj_in: ProductCreate):
        """Validation hook called automatically from BaseController.create()"""
        pass