from flask import Blueprint, jsonify, request
from ..models import Orders, db
from ..schemas import order_schema, orders_schema

orders_bp = Blueprint('orders', __name__, url_prefix='/orders')

@orders_bp.route('/', methods=['GET'])
def get_orders():
    orders = Orders.query.all()
    return jsonify(orders_schema.dump(orders))

@orders_bp.route('/', methods=['POST'])
def create_order():
    data = request.get_json()

    try:
        data['cost'] = float(data['cost'])
        data['quantity'] = int(data['quantity'])
        data['vat'] = float(data['vat'])
        data['delivery_charges'] = float(data['delivery_charges'])
    except (ValueError, TypeError):
        return jsonify({'message': 'Invalid cost or quantity format'}), 400

    errors = order_schema.validate(data)
    if errors:
        return jsonify(errors), 400

    new_order = Orders(**data)
    db.session.add(new_order)
    db.session.commit()
    return jsonify(order_schema.dump(new_order)), 201

@orders_bp.route('/<int:id>', methods=['GET'])
def get_order(id):
    order = Orders.query.get_or_404(id)
    return jsonify(order_schema.dump(order))

@orders_bp.route('/<int:id>', methods=['PUT'])
def update_order(id):
    order = Orders.query.get_or_404(id)
    data = request.get_json()

    try:
        data['cost'] = float(data['cost'])
        data['quantity'] = int(data['quantity'])
    except (ValueError, TypeError):
        return jsonify({'message': 'Invalid cost or quantity format'}), 400

    errors = order_schema.validate(data)
    if errors:
        return jsonify(errors), 400

    Orders.query.filter_by(id=id).update(data)
    db.session.commit()
    return jsonify(order_schema.dump(order))

@orders_bp.route('/<int:ID>', methods=['DELETE'])
def delete_order(ID):
    order = Orders.query.get_or_404(ID)
    
    if order.received:
        return jsonify({'message': 'Cannot delete order with received items'}), 400
    
    db.session.delete(order)
    db.session.commit()
    return jsonify({'message': 'Order deleted successfully'}), 200

@orders_bp.route('/<int:ID>/status', methods=['PUT'])
def update_order_status(ID):
    order = Orders.query.get_or_404(ID)
    data = request.get_json()

    if 'status' not in data:
        return jsonify({'message': 'Status is required'}), 400

    order.status = data['status']
    db.session.commit()
    return jsonify(order_schema.dump(order))
