from flask import Blueprint, jsonify, request
from app.models import Orders, db,User
from app.schemas import order_schema, orders_schema
from flask_jwt_extended import jwt_required, get_jwt_identity
from flask_jwt_extended.exceptions import NoAuthorizationError

orders_bp = Blueprint('orders', __name__, url_prefix='/orders')

@orders_bp.errorhandler(NoAuthorizationError)
def handle_missing_token(error):
    return jsonify({'message': 'JWT token is missing or invalid'}), 401

@orders_bp.route('/', methods=['GET'])
@jwt_required()
def get_orders():
    orders = Orders.query.all()
    return jsonify(orders_schema.dump(orders))

@orders_bp.route('/', methods=['POST'])
@jwt_required()
def create_order():
    current_user = get_jwt_identity()
    data = request.get_json()

    if not data:
        return jsonify({'message': 'No data provided'}), 400

    # Ensure the current user ID is included
    data['user_id'] = current_user

    # Check if user exists in the database
    user = User.query.get(current_user)
    if not user:
        return jsonify({'error': f'User with id {current_user} does not exist'}), 400

    # Validate and convert data types
    try:
        data['cost'] = float(data.get('cost', 0))
        data['quantity'] = int(data.get('quantity', 0))
        data['vat'] = float(data.get('vat', 0))
        data['delivery_charges'] = float(data.get('delivery_charges', 0))
    except ValueError:
        return jsonify({'message': 'Invalid cost, quantity, vat, or delivery_charges format'}), 400

    errors = order_schema.validate(data)
    if errors:
        return jsonify(errors), 400


    try:
        new_order = Orders(**data)
        db.session.add(new_order)
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500  # Return any database error

    return jsonify(order_schema.dump(new_order)), 201



@orders_bp.route('/<int:id>', methods=['GET'])
@jwt_required()
def get_order(id):
    order = Orders.query.get_or_404(id)
    return jsonify(order_schema.dump(order))

from flask_jwt_extended import jwt_required, get_jwt_identity

@orders_bp.route('/<int:id>', methods=['PUT'])
@jwt_required()
def update_order(id):
    user_id = get_jwt_identity()

    order = Orders.query.get_or_404(id)

    data = request.get_json()
    data['user_id'] = user_id

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

@orders_bp.route('/<int:id>', methods=['DELETE'])
@jwt_required()
def delete_order(id):
    order = Orders.query.get_or_404(id)
    
    if order.received:
        return jsonify({'message': 'Cannot delete order with received items'}), 400
    
    db.session.delete(order)
    db.session.commit()
    return jsonify({'message': 'Order deleted successfully'}), 200

@orders_bp.route('/<int:id>/status', methods=['PUT'])
@jwt_required()
def update_order_status(id):
    order = Orders.query.get_or_404(id)
    data = request.get_json()

    if 'status' not in data:
        return jsonify({'message': 'Status is required'}), 400

    order.status = data['status']
    db.session.commit()
    return jsonify(order_schema.dump(order))
