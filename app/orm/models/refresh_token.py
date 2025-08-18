from time import timezone
from ..database import db
from datetime import datetime, timedelta

class Refresh_Token(db.Model):
    __tablename__ = "refresh_token"

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)
    token_hash = db.Column(db.String(255), nullable=False)
    device_info = db.Column(db.String(255), nullable=True)
    expires_at = db.Column(db.DateTime(timezone=True), nullable=False, default=lambda: datetime.now(timezone.utc) + timedelta(days=30))
    register = db.Column(db.DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))
    updated = db.Column(db.DateTime(timezone=True), default=lambda: datetime.now(timezone.utc),
                      onupdate=lambda: datetime.now(timezone.utc))

    # Relationships
    user = db.relationship("User", back_populates="refresh_tokens")
    