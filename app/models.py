from .extensions import db

class Users(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False, unique=True)
    email = db.Column(db.String(100), nullable=False, unique=True)
    phone_number = db.Column(db.String(20),nullable=False)
    role_id = db.Column(db.Integer,nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)

    orders = db.relationship('Orders', back_populates='user', cascade="all, delete-orphan", lazy=True)

class Orders(db.Model):
    __tablename__ = 'orders'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    order_name = db.Column(db.String(50), nullable=False)
    order_description = db.Column(db.String(250), nullable=False)
    name = db.Column(db.String(50), nullable=False)
    cost = db.Column(db.Float, nullable=False)
    space = db.Column(db.String(50), nullable=False)
    vat = db.Column(db.Float, nullable=False)
    quantity = db.Column(db.Integer, nullable=False)
    status = db.Column(db.String(50), nullable=False)
    date_ordered = db.Column(db.Date, nullable=False)
    payment_status = db.Column(db.String(50), nullable=False)
    dispatch_status = db.Column(db.String(50), nullable=False)
    delivery_charges = db.Column(db.Float, nullable=True)
    reason = db.Column(db.String(50), nullable=True)
    initialiser = db.Column(db.String(50), nullable=True)

    user = db.relationship('Users', back_populates='orders')
    received = db.relationship('Received', back_populates='order', cascade="all, delete-orphan", lazy=True)

class Received(db.Model):
    __tablename__ = 'received'

    id = db.Column(db.Integer, primary_key=True)
    order_id = db.Column(db.Integer, db.ForeignKey('orders.id'), nullable=False)
    received_quantity = db.Column(db.Integer, nullable=False)
    date_received = db.Column(db.Date, nullable=False)

    order = db.relationship('Orders', back_populates='received')
