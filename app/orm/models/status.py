from ..database import db
from datetime import datetime, timezone

class Status(db.Model):
    __tablename__ = 'status'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    enable = db.Column(db.Boolean, default=True)
    register = db.Column(db.DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))
    updated = db.Column(db.DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), 
              onupdate=lambda: datetime.now(timezone.utc))

    payments = db.relationship('Payment', back_populates='status', lazy='dynamic')
