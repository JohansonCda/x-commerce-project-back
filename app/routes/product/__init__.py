from flask_restx import Namespace

products_ns = Namespace('product', description='Product operations')

from .get_all_products import *
from .products_id import *
from .create_products import *

__all__ = [
    "products_ns"
]