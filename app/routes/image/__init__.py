from flask_restx import Namespace

images_ns = Namespace('image', description='Image operations')

from .get_file_images import *
from .create_image import *
from .images_id import *

__all__ = [
    "images_ns"
]