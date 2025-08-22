from time import timezone
from ..database import db
from datetime import datetime

class Order(db.Model):
    __tablename__ = "order"

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)
    created_at = db.Column(db.DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), nullable=False)
    status = db.Column(db.String(50), nullable=False, default="pending")

  
    user = db.relationship("User", back_populates="orders")
    details = db.relationship("OrderDetail", back_populates="order", cascade="all, delete-orphan")
    pays = db.relationship("Pay", back_populates="order", lazy="dynamic")
