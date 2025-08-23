import os
from typing import List
from ..database import db
from flask import current_app
from pathlib import Path
from .base_controller import BaseController
from ..models.product_image import ProductImage
from ..schemas.product_image_schema import ProductImageCreate, ProductImageUpdate, ProductImageRead

class ProductImageController(BaseController[ProductImage, ProductImageCreate, ProductImageRead, ProductImageUpdate]):
    def __init__(self):
        super().__init__(ProductImage, ProductImageCreate, ProductImageRead, ProductImageUpdate)

    def get_by_products(self, product_ids: list[int]) -> List[ProductImageRead]:
        """Get all images for a list of product IDs"""
        if not product_ids:
            return []
        objs = (
            db.session.query(self.model)
            .filter(self.model.product_id.in_(product_ids))
            .all()
        )
        return [ProductImageRead.model_validate(obj) for obj in objs]
    
    def get_by_product_name(self, product_name: str) -> List[ProductImageRead]:
        """Get all images for a product by product name"""
        from ..models.product import Product
        objs = (
            db.session.query(self.model)
            .join(Product, self.model.product_id == Product.id)
            .filter(Product.name == product_name)
            .all()
        )
        return [ProductImageRead.model_validate(obj) for obj in objs]

    def get_by_product(self, product_id: int) -> List[ProductImageRead]:
        """Get all images for a product"""
        objs = (
            db.session.query(self.model)
            .filter(self.model.product_id == product_id)
            .all()
        )
        return [ProductImageRead.model_validate(obj) for obj in objs]

    def get_main_image(self, product_id: int) -> ProductImageRead | None:
        """Get the main image for a product, if any"""
        obj = (
            db.session.query(self.model)
            .filter(
                self.model.product_id == product_id,
                self.model.is_main == True
            )
            .first()
        )
        return ProductImageRead.model_validate(obj) if obj else None

    def register_image(self, product_id: int, filename: str, is_main: bool = False, alt: str | None = None) -> ProductImageRead:
        """
        Registers in the database an image that already exists in the filesystem.
        """
        ruta_db = os.path.join(current_app.config["UPLOAD_FOLDER"], filename)
        ruta_db = Path(ruta_db).as_posix()

        obj_in = ProductImageCreate(
            product_id=product_id,
            url=ruta_db,
            is_main=is_main,
            alt=alt
        )

        return self.create(obj_in)

    def _validate_create(self, obj_in: ProductImageCreate):
        """Validation hook called automatically from BaseController.create()"""
        pass
