from flask_restx import Namespace


payments_ns = Namespace('payment', description='Payment operations')

from .payments import *
from .payments_id import *

__all__ = [
    "payments_ns"
]