from flask import Flask

from api.api_resources import (
    Transaction,
    Chain,
    Supplier,
    Customer,
    Products,
    Inventory,
    Shipment,
)
from api.api_setup import (
    api,
)
from database.db import SupplyChainDatabase
from log_config.logging_config import logging_config

logging_config.configure_logger()
logging_config.configure_eliot()
logging_config.initialize_spinner()

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


@app.before_request
def before_request():
    logging_config.start_spinner()


@app.after_request
def after_request(response):
    logging_config.stop_spinner()
    return response


@api.errorhandler(Exception)
def handle_exception(error):
    return {"message": str(error)}, 500


if __name__ == "__main__":
    app.run(debug=True)
