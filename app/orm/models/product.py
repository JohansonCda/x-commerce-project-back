from datetime import datetime, timezone
from ..database import db

class Product(db.Model):
    __tablename__ = 'product'

    id = db.Column(db.BigInteger, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    description = db.Column(db.Text, nullable=True)
    price = db.Column(db.Numeric(10, 2), nullable=False)
    stock = db.Column(db.Integer, nullable=False)
    enable = db.Column(db.Boolean, default=True)
    register = db.Column(db.DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))
    updated = db.Column(db.DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), 
              onupdate=lambda: datetime.now(timezone.utc))