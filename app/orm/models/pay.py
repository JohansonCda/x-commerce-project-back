from ..database import db

class Pay(db.Model):
    __tablename__ = 'pay'

    id = db.Column(db.Integer, primary_key=True)
    order_id = db.Column(db.Integer, db.ForeignKey('order.id'), nullable=False)
    mount = db.Column(db.Float, nullable=False)
    pay_method = db.Column(db.String(50), nullable=False)
    status_id = db.Column(db.Integer, db.ForeignKey('status.id'), nullable=False)

    status = db.relationship('Status', back_populates='pays')
    order = db.relationship('Order', back_populates='pays')
