from flask import Flask

from api_resources import (
    Transaction,
    Chain,
    Supplier,
    Customer,
    Products,
    Inventory,
    Shipment,
)
from api_setup import (
    api,
)
from db import SupplyChainDatabase

app = Flask(__name__)
api.init_app(app)

# Initialize the database object
db = SupplyChainDatabase()

# Add the resources to the API
api.add_resource(Products, "/products", resource_class_kwargs={"db": db})
api.add_resource(Inventory, "/inventory", resource_class_kwargs={"db": db})
api.add_resource(Shipment, "/shipments", resource_class_kwargs={"db": db})
api.add_resource(Transaction, "/transactions", resource_class_kwargs={"db": db})
api.add_resource(Chain, "/chain", resource_class_kwargs={"db": db})
api.add_resource(Supplier, "/supplier", resource_class_kwargs={"db": db})
api.add_resource(Customer, "/customer", resource_class_kwargs={"db": db})


@api.errorhandler(Exception)
def handle_exception(error):
    return {"message": str(error)}, 500


if __name__ == "__main__":
    app.run(debug=True)
