from .extensions import db

class Orders(db.Model):
    __tablename__ = 'orders'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    cost = db.Column(db.Float, nullable=False)
    quantity = db.Column(db.Integer, nullable=False)
    status = db.Column(db.String(50), nullable=False)
    date_ordered = db.Column(db.Date, nullable=False)

    received = db.relationship('Received', back_populates='orders', cascade="all, delete-orphan", lazy=True)

class Received(db.Model):
    __tablename__ = 'received'

    id = db.Column(db.Integer, primary_key=True)
    order_id = db.Column(db.Integer, db.ForeignKey('orders.id'), nullable=False)
    received_quantity = db.Column(db.Integer, nullable=False)
    date_received = db.Column(db.Date, nullable=False)

    orders = db.relationship('Orders', back_populates='received')
