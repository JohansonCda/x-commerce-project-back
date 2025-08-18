from datetime import datetime, timezone
from ..database import db

class User(db.Model):
	__tablename__ = 'user'

	id = db.Column(db.BigInteger, primary_key=True)
	username = db.Column(db.String(100), nullable=False, unique=True)
	full_name = db.Column(db.String(100), nullable=False)
	email = db.Column(db.String(100), nullable=False, unique=True)
	password = db.Column(db.String(100), nullable=False)
	phone = db.Column(db.String(15), nullable=False)
	enable = db.Column(db.Boolean, default=True)
	is_admin = db.Column(db.Boolean, default=False)
	register = db.Column(db.DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))
	updated = db.Column(db.DateTime(timezone=True), default=lambda: datetime.now(timezone.utc),
						onupdate=lambda: datetime.now(timezone.utc))

    # Relationships
	#products = db.relationship('Product', back_populates='category', lazy='dynamic')
	orders = db.relationship('Order', back_populates='user', lazy='dynamic')
	refresh_tokens = db.relationship('Refresh_Token', back_populates='user', lazy='dynamic')