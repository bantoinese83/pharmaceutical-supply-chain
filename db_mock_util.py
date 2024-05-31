import random
from faker import Faker
from api_resources import db

# Initialize faker generator
fake = Faker()

# Define the number of entries to generate
num_entries = 400

# Generate suppliers and customers first
suppliers = []
customers = []

for _ in range(num_entries):
    supplier = {
        "name": fake.company(),
        "address": fake.address(),
    }
    supplier = db.insert_supplier(supplier)
    suppliers.append(supplier)

    customer = {
        "name": fake.name(),
        "address": fake.address(),
    }
    customer = db.insert_customer(customer)
    customers.append(customer)

# Generate products, inventory, transactions, and shipments
for _ in range(num_entries):
    product_id = ''.join(random.choices('0123456789', k=6))
    product = {
        "product_id": product_id,
        "name": fake.catch_phrase(),
        "description": fake.bs(),
        "price": random.uniform(10, 1000),
    }
    db.insert_product(product)

    quantity = random.randint(1, 100)
    inventory = {
        "product_id": product_id,
        "quantity": quantity,
    }
    db.insert_inventory(inventory)

    supplier_id = suppliers[random.randint(0, len(suppliers) - 1)]['id']
    customer_id = customers[random.randint(0, len(customers) - 1)]['id']
    # Check if supplier_id is not None
    if supplier_id is not None:
        transaction_detail = fake.sentence(nb_words=5)
        shipment_date = fake.date(pattern="%Y-%m-%d", end_datetime=None)
        expected_delivery_date = fake.date(pattern="%Y-%m-%d", end_datetime=None)
        transaction = {
            "product_id": product_id,
            "transaction_detail": transaction_detail,
            "supplier_id": supplier_id,
            "customer_id": customer_id,
            "quantity": quantity,
            "shipment_date": shipment_date,
            "expected_delivery_date": expected_delivery_date,
        }
        db.insert_transaction(transaction)

        shipment = {
            "supplier_id": supplier_id,
            "customer_id": customer_id,
            "product_id": product_id,
            "quantity": quantity,
            "shipment_date": shipment_date,
            "expected_delivery_date": expected_delivery_date,
        }
        db.insert_shipment(shipment)
