from flask import request
from flask_restx import Resource

from api.api_setup import (
    api,
    ns_blockchain,
    ns_transactions,
    ns_products,
    ns_inventory,
    ns_shipments,
    ns_supplier,
    ns_customer,
)
from blockchain import blockchain
from database.db import db
from models.models import block_model, supplier_model, customer_model, shipment_model
from api.validation_utils import Validator, ValidationError


@api.doc(tags=["blockchain"])
@ns_blockchain.route("/create_transaction")
class Transaction(Resource):
    @ns_blockchain.expect(block_model)
    def post(self):
        try:
            required_fields = [
                "product_id",
                "transaction_detail",
                "supplier_id",
                "customer_id",
                "quantity",
                "shipment_date",
                "expected_delivery_date",
            ]
            if not all(field in api.payload for field in required_fields):
                return {"message": "All fields are required"}, 400

            product_id = api.payload["product_id"]
            transaction_detail = api.payload["transaction_detail"]
            supplier_id = api.payload["supplier_id"]
            customer_id = api.payload["customer_id"]
            quantity = api.payload["quantity"]
            shipment_date = api.payload["shipment_date"]
            expected_delivery_date = api.payload["expected_delivery_date"]

            # Use the Validator class for validation
            Validator.validate_product_id(product_id)
            Validator.validate_transaction_detail(transaction_detail)
            Validator.validate_supplier_id(supplier_id)
            Validator.validate_customer_id(customer_id)
            Validator.validate_quantity(quantity)
            Validator.validate_date(shipment_date)
            Validator.validate_date(expected_delivery_date)

            block_data = {
                "product_id": product_id,
                "transaction_detail": transaction_detail,
                "supplier_id": supplier_id,
                "customer_id": customer_id,
                "quantity": quantity,
                "shipment_date": shipment_date,
                "expected_delivery_date": expected_delivery_date,
            }
            # Insert the transaction into the database
            db.insert_transaction(block_data)
            # Use the blockchain instance to add a block
            blockchain.blockchain.add_block(block_data)
            return {"message": "Transaction recorded successfully"}, 200
        except ValidationError as e:
            return {"message": str(e)}, 400
        except Exception as e:
            return {
                "message": f"An error occurred while processing the transaction: {str(e)}"
            }, 500


@api.doc(tags=["blockchain"])
@ns_blockchain.route("/get_chain")
class Chain(Resource):
    @staticmethod
    def get():
        chain_data = []
        for block in blockchain.blockchain.blockchain:
            chain_data.append(
                {
                    "index": block.index,
                    "timestamp": block.timestamp,
                    "data": block.data,
                    "hash": block.block_hash,
                    "previous_hash": block.previous_hash,
                }
            )
        return {"length": len(chain_data), "chain": chain_data}, 200


@api.doc(tags=["blockchain"])
@ns_blockchain.route("/get_block_by_index/<int:index>")
class BlockByIndex(Resource):
    @staticmethod
    def get(index):
        block = next(
            (block for block in blockchain.blockchain if block.index == index), None
        )
        if block is None:
            return {"message": "Block not found"}, 404
        return block.__dict__, 200


@api.doc(tags=["blockchain"])
@ns_blockchain.route("/get_block_by_hash/<string:hash>")
class BlockByHash(Resource):
    @staticmethod
    def get(_hash):
        block = next(
            (block for block in blockchain.blockchain if block.block_hash == _hash), None
        )
        if block is None:
            return {"message": "Block not found"}, 404
        return block.__dict__, 200


@api.doc(tags=["transactions"])
@ns_transactions.route("/transactions/<int:id>")
class TransactionByID(Resource):
    @staticmethod
    def get(_id):
        transaction = db.get_transaction_by_id(_id)
        if transaction is None:
            return {"message": "Transaction not found"}, 404
        return transaction, 200


@api.doc(tags=["supplier"])
@ns_supplier.route("/create_supplier")
class Supplier(Resource):
    @staticmethod
    @ns_supplier.expect(supplier_model)
    def post():
        supplier = api.payload
        db.insert_supplier(supplier)
        return {"message": "Supplier added successfully"}, 201


@api.doc(tags=["customer"])
@ns_customer.route("/create_customer")
class Customer(Resource):
    @staticmethod
    @ns_customer.expect(customer_model)
    def post():
        customer = api.payload
        db.insert_customer(customer)
        return {"message": "Customer added successfully"}, 201


@api.doc(tags=["products"])
@ns_products.route("/get_all_products")
class Products(Resource):
    @staticmethod
    def get():
        products = db.get_all_products()
        return {"products": products}, 200


@api.doc(tags=["products"])
@ns_products.route("/get_product_by_id/<int:id>")
class ProductByID(Resource):
    @staticmethod
    def get(_id):
        product = db.get_product_by_id(_id)
        if product is None:
            return {"message": "Product not found"}, 404
        return product, 200


@api.doc(tags=["inventory"])
@ns_inventory.route("/get_all_inventory")
class Inventory(Resource):
    @staticmethod
    def get():
        inventory = db.get_inventory()
        return {"inventory": inventory}, 200


@api.doc(tags=["inventory"])
@ns_inventory.route("/get_inventory_by_product_id/<int:product_id>")
class InventoryByProductID(Resource):
    @staticmethod
    def get(product_id):
        inventory = db.get_inventory_by_product_id(product_id)
        if inventory is None:
            return {"message": "Inventory not found"}, 404
        return inventory, 200


@api.doc(tags=["shipments"])
@ns_shipments.route("/create_shipment")
class Shipment(Resource):
    @api.expect(shipment_model)
    def post(self):
        if request.headers.get('Content-Type') != 'application/json':
            return {"message": "Unsupported Media Type: Content-Type must be 'application/json'"}, 415
        shipment = api.payload
        db.insert_shipment(shipment)
        return {"message": "Shipment added successfully"}, 201


@api.doc(tags=["transactions"])
@ns_transactions.route("/get_all_transactions")
class Transactions(Resource):
    @staticmethod
    def get():
        transactions = db.get_all_transactions()
        return {"transactions": transactions}, 200
