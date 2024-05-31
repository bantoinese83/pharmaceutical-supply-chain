import logging
import sqlite3

from database.db_config import DatabaseConfig
from log_config.logging_config import LoggingConfig


class SupplyChainDatabase:
    def __init__(self):
        self.db_config = DatabaseConfig()
        self.db_name = self.db_config.DB_CONFIG[self.db_config.DB_TYPE]
        self.logging_config = LoggingConfig()
        self.logging_config.configure_logger()
        self.logging_config.configure_eliot()
        self.spinner = self.logging_config.initialize_spinner()

    def _execute_query(self, query, params=None):
        connection = sqlite3.connect(self.db_name)
        cursor = connection.cursor()

        # Check if the tables already exist
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='transactions'")
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='suppliers'")
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='customers'")
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='products'")
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='inventory'")
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='shipments'")
        if cursor.fetchone():
            print("Database is already set up.")
            return

        try:
            if params:
                cursor.execute(query, params)
            else:
                cursor.execute(query)
            connection.commit()
        except sqlite3.Error:
            logging.basicConfig(filename='logs/python_logger.log', level=logging.INFO)
        finally:
            connection.close()

    def create_database(self):
        connection = None
        try:
            self.spinner.start("Creating database...")
            connection = sqlite3.connect(self.db_name)
            cursor = connection.cursor()
            cursor.execute(
                """
                CREATE TABLE IF NOT EXISTS transactions (
                    id INTEGER PRIMARY KEY,
                    product_id TEXT NOT NULL,
                    transaction_detail TEXT NOT NULL,
                    supplier_id INTEGER NOT NULL,
                    customer_id INTEGER NOT NULL,
                    quantity INTEGER NOT NULL,
                    shipment_date TEXT NOT NULL,
                    expected_delivery_date TEXT NOT NULL
                )
            """
            )
            cursor.execute(
                """
                CREATE TABLE IF NOT EXISTS suppliers (
                    id INTEGER PRIMARY KEY,
                    name TEXT NOT NULL,
                    address TEXT NOT NULL
                )
            """
            )
            cursor.execute(
                """
                CREATE TABLE IF NOT EXISTS customers (
                    id INTEGER PRIMARY KEY,
                    name TEXT NOT NULL,
                    address TEXT NOT NULL
                )
            """
            )
            cursor.execute(
                """
                CREATE TABLE IF NOT EXISTS products (
                    id INTEGER PRIMARY KEY,
                    product_id TEXT NOT NULL,
                    name TEXT NOT NULL,
                    description TEXT NOT NULL,
                    price REAL NOT NULL
                )
            """
            )
            cursor.execute(
                """
                CREATE TABLE IF NOT EXISTS inventory (
                    id INTEGER PRIMARY KEY,
                    product_id TEXT NOT NULL,
                    quantity INTEGER NOT NULL
                )
            """
            )
            cursor.execute(
                """
                CREATE TABLE IF NOT EXISTS shipments (
                    id INTEGER PRIMARY KEY,
                    supplier_id INTEGER NOT NULL,
                    customer_id INTEGER NOT NULL,
                    product_id TEXT NOT NULL,
                    quantity INTEGER NOT NULL,
                    shipment_date TEXT NOT NULL,
                    expected_delivery_date TEXT NOT NULL
                )
            """
            )
            self.spinner.succeed("Database created successfully.")
        except sqlite3.Error as e:
            print("Error creating database:", e)
        finally:
            if connection:
                connection.close()

    def insert_transaction(self, transaction):
        query = """
            INSERT INTO transactions (product_id, transaction_detail, supplier_id, customer_id, quantity, shipment_date, 
            expected_delivery_date)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        """
        connection = sqlite3.connect(self.db_name)
        cursor = connection.cursor()
        cursor.execute(query, (
            transaction["product_id"],
            transaction["transaction_detail"],
            transaction["supplier_id"],
            transaction["customer_id"],
            transaction["quantity"],
            transaction["shipment_date"],
            transaction["expected_delivery_date"],
        ))
        transaction_id = cursor.lastrowid
        connection.commit()
        connection.close()
        transaction['id'] = transaction_id
        return transaction

    def insert_supplier(self, supplier):
        query = """
            INSERT INTO suppliers (name, address) VALUES (?, ?)
        """
        connection = sqlite3.connect(self.db_name)
        cursor = connection.cursor()
        cursor.execute(query, (supplier["name"], supplier["address"]))
        supplier_id = cursor.lastrowid
        connection.commit()
        connection.close()
        supplier['id'] = supplier_id
        return supplier

    def insert_customer(self, customer):
        query = """
            INSERT INTO customers (name, address) VALUES (?, ?)
        """
        connection = sqlite3.connect(self.db_name)
        cursor = connection.cursor()
        cursor.execute(query, (customer["name"], customer["address"]))
        customer_id = cursor.lastrowid
        connection.commit()
        connection.close()
        customer['id'] = customer_id
        return customer

    def insert_product(self, product):
        query = """
            INSERT INTO products (product_id, name, description, price)
            VALUES (?, ?, ?, ?)
        """
        connection = sqlite3.connect(self.db_name)
        cursor = connection.cursor()
        cursor.execute(query, (
            product["product_id"],
            product["name"],
            product["description"],
            product["price"],
        ))
        product_id = cursor.lastrowid
        connection.commit()
        connection.close()
        product['id'] = product_id
        return product

    def insert_inventory(self, inventory):
        query = """
         INSERT INTO inventory (product_id, quantity)
         VALUES (?, ?)
        """
        connection = sqlite3.connect(self.db_name)
        cursor = connection.cursor()
        cursor.execute(query, (
            inventory["product_id"],
            inventory["quantity"],
        ))
        inventory_id = cursor.lastrowid
        connection.commit()
        connection.close()
        inventory['id'] = inventory_id
        return inventory

    def insert_shipment(self, shipment):
        query = """
            INSERT INTO shipments (supplier_id, customer_id, product_id, quantity, 
            shipment_date, expected_delivery_date)
            VALUES (?, ?, ?, ?, ?, ?)
        """
        connection = sqlite3.connect(self.db_name)
        cursor = connection.cursor()
        cursor.execute(query, (
            shipment["supplier_id"],
            shipment["customer_id"],
            shipment["product_id"],
            shipment["quantity"],
            shipment["shipment_date"],
            shipment["expected_delivery_date"],
        ))
        shipment_id = cursor.lastrowid
        connection.commit()
        connection.close()
        shipment['id'] = shipment_id
        return shipment

    def get_transaction_by_id(self, transaction_id):
        connection = sqlite3.connect(self.db_name)
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM transactions WHERE id = ?", (transaction_id,))
        transaction = cursor.fetchone()
        connection.close()
        return transaction

    def get_inventory(self):
        connection = sqlite3.connect(self.db_name)
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM inventory")
        inventory = cursor.fetchall()
        connection.close()
        return inventory

    def get_all_products(self):
        connection = sqlite3.connect(self.db_name)
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM products")
        products = cursor.fetchall()
        connection.close()
        return products


# Initialize the database object
db = SupplyChainDatabase()

# Call the function to create the database
db.create_database()
