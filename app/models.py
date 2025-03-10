from .extensions import db

class User(db.Model):
    __tablename__ = 'user'  

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False, unique=True)
    email = db.Column(db.String(100), nullable=False, unique=True)
    phone_number = db.Column(db.String(20), nullable=False)
    role_id = db.Column(db.Integer, nullable=False)
    password = db.Column(db.String(255), nullable=False)

    orders = db.relationship('Orders', back_populates='user', cascade="all, delete-orphan", lazy=True)


class Orders(db.Model):
    __tablename__ = 'orders'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    order_name = db.Column(db.String(50), nullable=False)
    order_description = db.Column(db.String(250), nullable=False)
    name = db.Column(db.String(50), nullable=False)
    cost = db.Column(db.Float, nullable=False)
    vendor_id = db.Column(db.Integer, db.ForeignKey('vendors.id'), nullable=False)
    vat = db.Column(db.Float, nullable=False)
    quantity = db.Column(db.Integer, nullable=False)
    status = db.Column(db.String(50), nullable=False)
    date_ordered = db.Column(db.Date, nullable=False)
    payment_status = db.Column(db.String(50), nullable=False)
    dispatch_status = db.Column(db.String(50), nullable=False)
    delivery_charges = db.Column(db.Float, nullable=True)
    reason = db.Column(db.String(50), nullable=True)
    initialiser = db.Column(db.String(50), nullable=True)

    user = db.relationship('User', back_populates='orders') 
    received = db.relationship('Received', back_populates='order', cascade="all, delete-orphan", lazy=True)
    vendor = db.relationship('Vendor', back_populates='orders')


class Vendor(db.Model):
    __tablename__ = "vendors"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    email = db.Column(db.String(255), unique=True, nullable=False)
    phone = db.Column(db.String(20), nullable=False)
    bio = db.Column(db.Text)
    kra_pin = db.Column(db.String(255), nullable=False)
    status = db.Column(db.Boolean, default=False)
    address = db.Column(db.Text)
    city = db.Column(db.String(255))
    postal_code = db.Column(db.String(255))
    county = db.Column(db.String(255), nullable=False)
    country = db.Column(db.String(255), nullable=False)
    bank_name = db.Column(db.String(255), nullable=False)
    account_number = db.Column(db.String(255), nullable=False)
    mpesa_paybill = db.Column(db.String(255))
    buy_goods_till = db.Column(db.String(255))
    contact_person_name = db.Column(db.String(255))
    contact_person_email = db.Column(db.String(255))
    contact_person_phone = db.Column(db.String(20))

    orders = db.relationship('Orders', back_populates='vendor', lazy='dynamic')


class Received(db.Model):
    __tablename__ = 'received'

    id = db.Column(db.Integer, primary_key=True)
    order_id = db.Column(db.Integer, db.ForeignKey('orders.id'), nullable=False)
    received_quantity = db.Column(db.Integer, nullable=False)
    date_received = db.Column(db.Date, nullable=False)

    order = db.relationship('Orders', back_populates='received')
