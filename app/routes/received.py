from flask_jwt_extended.exceptions import NoAuthorizationError
from flask import Blueprint, jsonify, request
from app.models import Orders, Received, db
from app.schemas import received_schema, receiveds_schema


received_bp = Blueprint('received', __name__, url_prefix='/received')

@received_bp.errorhandler(NoAuthorizationError)
def handle_missing_token(error):
    return jsonify({'message': 'JWT token is missing or invalid'}), 401

@received_bp.route('/', methods=['GET'])
def get_all_received():
    received = Received.query.all()
    return jsonify(receiveds_schema.dump(received))

@received_bp.route('/', methods=['POST'])
def create_received():
    data = request.get_json()

    try:
        data['order_id'] = int(data['order_id'])
        data['received_quantity'] = int(data['received_quantity'])
    except (ValueError, TypeError):
        return jsonify({'message': 'Invalid order_id or received_quantity format'}), 400

    order = Orders.query.get(data['order_id'])
    if not order:
        return jsonify({'message': 'Order not found'}), 404

    errors = received_schema.validate(data)
    if errors:
        return jsonify(errors), 400

    new_received = Received(**data)
    db.session.add(new_received)
    db.session.commit()

    return jsonify(received_schema.dump(new_received)), 201

@received_bp.route('/<int:id>', methods=['GET'])
def get_received(id):
    received = Received.query.get_or_404(id)
    return jsonify(received_schema.dump(received))
