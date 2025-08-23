from .image import images_ns
from .main_routes import main_ns
from .auth_routes import auth_ns
from .product import products_ns
from .category import categories_ns
from .payment import payments_ns

__all__ = [
    "images_ns",
    "main_ns",
    "auth_ns",
    "products_ns",
    "categories_ns",
    "payments_ns"
]