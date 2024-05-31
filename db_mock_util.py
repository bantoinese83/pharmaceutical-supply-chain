import random
from faker import Faker

from api_resources import db

# Initialize faker generator
fake = Faker()

# Define the number of entries to generate
num_entries = 10000

for _ in range(num_entries):
    # Generate fake data for each field
    product_id = ''.join(random.choices('0123456789', k=6))
    transaction_detail = fake.sentence(nb_words=5)
    supplier_id = random.randint(1, 100)
    customer_id = random.randint(1, 100)
    quantity = random.randint(1, 100)
    shipment_date = fake.date(pattern="%Y-%m-%d", end_datetime=None)
    expected_delivery_date = fake.date(pattern="%Y-%m-%d", end_datetime=None)

    # Create a dictionary with the generated data
    transaction = {
        "product_id": product_id,
        "transaction_detail": transaction_detail,
        "supplier_id": supplier_id,
        "customer_id": customer_id,
        "quantity": quantity,
        "shipment_date": shipment_date,
        "expected_delivery_date": expected_delivery_date,
    }

    # Insert the transaction into the database
    db.insert_transaction(transaction)

    # Generate fake data for supplier
    supplier = {
        "name": fake.company(),
        "address": fake.address(),
    }

    # Insert the supplier into the database
    db.insert_supplier(supplier)

    # Generate fake data for customer
    customer = {
        "name": fake.name(),
        "address": fake.address(),
    }

    # Insert the customer into the database
    db.insert_customer(customer)

    # Generate fake data for product
    product = {
        "product_id": ''.join(random.choices('0123456789ABCDEF', k=6)),
        "name": fake.catch_phrase(),
        "description": fake.bs(),
        "price": random.uniform(10, 1000),
    }

    # Insert the product into the database
    db.insert_product(product)

    # Generate fake data for inventory
    inventory = {
        "product_id": product_id,
        "quantity": quantity,
    }

    # Insert the inventory into the database
    db.insert_inventory(inventory)

    # Generate fake data for shipment
    shipment = {
        "supplier_id": supplier_id,
        "customer_id": customer_id,
        "product_id": product_id,
        "quantity": quantity,
        "shipment_date": shipment_date,
        "expected_delivery_date": expected_delivery_date,
    }

    # Insert the shipment into the database
    db.insert_shipment(shipment)
