from flask_restx import Namespace

users_ns = Namespace('user', description='User operations')

from .get_all_users import *
from .users_id import *
from .create_users import *

__all__ = [
    "users_ns"
]
