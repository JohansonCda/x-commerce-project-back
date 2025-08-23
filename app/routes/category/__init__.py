from flask_restx import Namespace

categories_ns = Namespace('category', description='Category operations')

from .categories import *
from .categories_id import *

__all__ = [
    "categories_ns"
]