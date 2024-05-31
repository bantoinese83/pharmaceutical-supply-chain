from flask_restx import Api

api = Api(
    version="1.0",
    title="Pharmaceutical Supply Chain Tracking API",
    description="A simple API for tracking pharmaceutical products throughout the supply chain",
)

ns_blockchain = api.namespace("blockchain", description="Blockchain operations")
ns_transactions = api.namespace("transactions", description="Transaction operations")
ns_products = api.namespace("products", description="Product operations")
ns_inventory = api.namespace("inventory", description="Inventory operations")
ns_shipments = api.namespace("shipments", description="Shipment operations")
ns_supplier = api.namespace("supplier", description="Supplier operations")
ns_customer = api.namespace("customer", description="Customer operations")
