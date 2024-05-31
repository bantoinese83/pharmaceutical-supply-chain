import random
from datetime import datetime, timedelta

import logging

from faker import Faker

from database.db import db
from log_config.logging_config import logging_config

logging_config.configure_logger()
logging_config.configure_eliot()
logging_config.initialize_spinner()

# Initialize faker generator
fake = Faker()

# Define the number of entries to generate
num_entries = 5000

# Generate suppliers and customers first
suppliers = []
customers = []

for i in range(num_entries):
    supplier = {
        "name": fake.company(),
        "address": fake.address(),
    }
    try:
        supplier = db.insert_supplier(supplier)
        suppliers.append(supplier)
        logging.info(f'Supplier {supplier["name"]} inserted successfully.')
    except Exception as e:
        logging.error(f'An error occurred while inserting supplier: {e}')

    customer = {
        "name": fake.name(),
        "address": fake.address(),
    }
    try:
        customer = db.insert_customer(customer)
        customers.append(customer)
        logging.info(f'Customer {customer["name"]} inserted successfully.')
    except Exception as e:
        logging.error(f'An error occurred while inserting customer: {e}')

        # Log progress of supplier and customer generation
    if (i + 1) % 100 == 0:
        logging.info(f'Generated {i + 1} suppliers and customers')

# Check if suppliers and customers are not empty
if not suppliers:
    raise ValueError("No suppliers were inserted")

if not customers:
    raise ValueError("No customers were inserted")

spinner = logging_config.initialize_spinner()
spinner.start()

# Generate products, inventory, transactions, and shipments
for i in range(num_entries):

    # Get tomorrow's date
    tomorrow = datetime.now() + timedelta(days=1)

    # Get a date 30 days from now
    end_date = datetime.now() + timedelta(days=30)

    # Generate shipment_date and expected_delivery_date
    shipment_date = fake.date_between_dates(date_start=tomorrow, date_end=end_date)

    # Convert shipment_date to a datetime object for comparison
    shipment_date_obj = datetime.strptime(str(shipment_date), "%Y-%m-%d")

    # Get a date 30 days from shipment_date
    end_date_from_shipment = shipment_date_obj + timedelta(days=30)

    # Generate expected_delivery_date between shipment_date and end_date_from_shipment
    expected_delivery_date = fake.date_between_dates(date_start=shipment_date_obj, date_end=end_date_from_shipment)

    # Convert expected_delivery_date to datetime object for comparison
    expected_delivery_date_obj = datetime.strptime(str(expected_delivery_date), "%Y-%m-%d")

    # Check if expected_delivery_date is before shipment_date
    if expected_delivery_date_obj < shipment_date_obj:
        raise ValueError("Expected delivery date cannot be before shipment date")

        # Log progress of product, inventory, transaction, and shipment generation
    if (i + 1) % 100 == 0:
        logging.info(f'Generated {i + 1} products, inventories, transactions, and shipments')

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
        spinner.stop()
