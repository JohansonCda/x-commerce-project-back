from ..database import db
from datetime import datetime, timezone

class ProductImage(db.Model):
    __tablename__ = 'product_image'
    
    id = db.Column(db.BigInteger, primary_key=True)
    url = db.Column(db.String(512), nullable=False)
    alt = db.Column(db.String(255), nullable=True)
    is_main = db.Column(db.Boolean, default=False)
    product_id = db.Column(db.BigInteger, db.ForeignKey('product.id'), nullable=False)
    register = db.Column(db.DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))
    updated = db.Column(db.DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), 
              onupdate=lambda: datetime.now(timezone.utc))

    product = db.relationship('Product', back_populates='images')