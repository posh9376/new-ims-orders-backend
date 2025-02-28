from marshmallow import Schema, fields

class OrdersSchema(Schema):
    id = fields.Int(dump_only=True)
    order_name = fields.Str(required=True)
    order_description = fields.Str(required=True)
    name = fields.Str(required=True)
    cost = fields.Float(required=True, validate=lambda x: x >= 0)
    space = fields.Str(required=True)
    vat = fields.Float(required=True)
    quantity = fields.Int(required=True, validate=lambda x: x > 0)
    status = fields.Str(required=True)
    date_ordered = fields.Date(required=True)
    payment_status = fields.Str(required=True)
    dispatch_status = fields.Str(required=True)
    delivery_charges = fields.Float(required=False)
    reason = fields.Str(required=False)
    initialiser = fields.Str(required=False)

class ReceivedSchema(Schema):
    id = fields.Int(dump_only=True)
    order_id = fields.Int(required=True)
    received_quantity = fields.Int(required=True, validate=lambda x: x > 0)
    date_received = fields.Date(required=True)

    orders = fields.Nested(OrdersSchema, only=("id", "name", "cost", "quantity", "status", "date_ordered"))

# Schema Instances
order_schema = OrdersSchema()
orders_schema = OrdersSchema(many=True)
received_schema = ReceivedSchema()
receiveds_schema = ReceivedSchema(many=True)
