from flask_restx import fields

from api_setup import api

block_model = api.model('Block', {
    'product_id': fields.String(required=True, description='The product id', example='P12345'),
    'transaction_detail': fields.String(required=True, description='The transaction detail', example='Purchase of 100 '
                                                                                                     'units of '
                                                                                                     'Product P12345'),
    'supplier_id': fields.Integer(required=True, description='The supplier id', example=101),
    'customer_id': fields.Integer(required=True, description='The customer id', example=202),
    'quantity': fields.Integer(required=True, description='The quantity of the product', example=100),
    'shipment_date': fields.String(required=True, description='The date of the shipment', example='2022-12-01'),
    'expected_delivery_date': fields.String(required=True, description='The expected delivery date of the shipment',
                                            example='2022-12-10'),
})

shipment_model = api.model(
    "Shipment",
    {
        "supplier_id": fields.Integer(required=True, description="The supplier id", example=101),
        "customer_id": fields.Integer(required=True, description="The customer id", example=202),
        "product_id": fields.String(required=True, description="The product id", example="P12345"),
        "quantity": fields.Integer(required=True, description="The quantity", example=100),
        "shipment_date": fields.String(required=True, description="The shipment date", example="2022-12-01"),
        "expected_delivery_date": fields.String(required=True, description="The expected delivery date",
                                                example="2022-12-10"),
    },
)

product_model = api.model(
    "Product",
    {
        "product_id": fields.String(required=True, description="The product id", example="P12345"),
        "name": fields.String(required=True, description="The name of the product", example="Product P12345"),
        "description": fields.String(required=True, description="The description of the product", example="This is a "),
        "price": fields.Float(required=True, description="The price of the product", example=100.0),
    },
)

supplier_model = api.model(
    "Supplier",
    {
        "name": fields.String(required=True, description="The name of the supplier", example="Supplier 1"),
        "address": fields.String(required=True, description="The address of the supplier", example="123 Main St"),
    },
)

customer_model = api.model(
    "Customer",
    {
        "name": fields.String(required=True, description="The name of the customer", example="Customer 1"),
        "address": fields.String(required=True, description="The address of the customer", example="456 Elm St"),
    },
)

inventory_model = api.model(
    "Inventory",
    {
        "product_id": fields.String(required=True, description="The product id", example="P12345"),
        "quantity": fields.Integer(required=True, description="The quantity of the product", example=100),
    },
)

transaction_model = api.model(
    "Transaction",
    {
        "product_id": fields.String(required=True, description="The product id", example="P12345"),
        "transaction_detail": fields.String(required=True, description="The transaction detail", example="Purchase of "
                                                                                                         "100 units "
                                                                                                         "of Product "
                                                                                                         "P12345"),
        "supplier_id": fields.Integer(required=True, description="The supplier id", example=101),
        "customer_id": fields.Integer(required=True, description="The customer id", example=202),
        "quantity": fields.Integer(required=True, description="The quantity of the product", example=100),
        "shipment_date": fields.String(required=True, description="The shipment date", example="2022-12-01"),
        "expected_delivery_date": fields.String(required=True, description="The expected delivery date",
                                                example="2022-12-10"),
    },
)
