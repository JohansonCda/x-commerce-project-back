
from ..database import db

class Category(db.Model):
	__tablename__ = 'category'

	id = db.Column(db.BigInteger, primary_key=True)
	name = db.Column(db.String(100), nullable=False, unique=True)
	description = db.Column(db.Text, nullable=True)
	enable = db.Column(db.Boolean, default=True)

	products = db.relationship('Product', back_populates='category', lazy='dynamic')
