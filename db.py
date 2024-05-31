import logging
import sqlite3
from time import sleep

from halo import Halo

spinner = Halo(
    text="Creating database...",
    spinner="dots",
)


class SupplyChainDatabase:
    def __init__(self, db_name="supply_chain.db"):
        self.db_name = db_name
        logging.basicConfig(level=logging.DEBUG)

    def _execute_query(self, query, params=None):
        connection = sqlite3.connect(self.db_name)
        cursor = connection.cursor()
        try:
            if params:
                cursor.execute(query, params)
            else:
                cursor.execute(query)
            connection.commit()
        except sqlite3.Error as e:
            logging.error("Error executing query: %s", e)
        finally:
            connection.close()

    def create_database(self):
        connection = None
        try:
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

            spinner.start("Creating database...")
            sleep(2)
            spinner.succeed("Database created successfully.")
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
        self._execute_query(
            query,
            (
                transaction["product_id"],
                transaction["transaction_detail"],
                transaction["supplier_id"],
                transaction["customer_id"],
                transaction["quantity"],
                transaction["shipment_date"],
                transaction["expected_delivery_date"],
            ),
        )

    def get_all_transactions(self):
        connection = sqlite3.connect(self.db_name)
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM transactions")
        transactions = cursor.fetchall()
        connection.close()
        return transactions

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

        # Add the id to the supplier dictionary and return it
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

        # Add the id to the customer dictionary and return it
        customer['id'] = customer_id
        return customer

    # ...

    def insert_product(self, product):
        query = """
            INSERT INTO products (product_id, name, description, price)
            VALUES (?, ?, ?, ?)
        """
        self._execute_query(
            query,
            (
                product["product_id"],
                product["name"],
                product["description"],
                product["price"],
            ),
        )

    def get_all_products(self):
        connection = sqlite3.connect(self.db_name)
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM products")
        products = cursor.fetchall()
        connection.close()
        return products

    def get_product_by_id(self, product_id):
        connection = sqlite3.connect(self.db_name)
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM products WHERE id = ?", (product_id,))
        product = cursor.fetchone()
        connection.close()
        return product

    def insert_inventory(self, inventory):
        query = """
         INSERT INTO inventory (product_id, quantity)
         VALUES (?, ?)
        """
        self._execute_query(
            query,
            (
                inventory["product_id"],
                inventory["quantity"],
            ),
        )

    def get_inventory(self):
        connection = sqlite3.connect(self.db_name)
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM inventory")
        inventory = cursor.fetchall()
        connection.close()
        return inventory

    def get_inventory_by_product_id(self, product_id):
        connection = sqlite3.connect(self.db_name)
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM inventory WHERE product_id = ?", (product_id,))
        inventory = cursor.fetchone()
        connection.close()
        return inventory

    def insert_shipment(self, shipment):
        query = """
            INSERT INTO shipments (supplier_id, customer_id, product_id, quantity, shipment_date, expected_delivery_date)
            VALUES (?, ?, ?, ?, ?, ?)
        """
        self._execute_query(
            query,
            (
                shipment["supplier_id"],
                shipment["customer_id"],
                shipment["product_id"],
                shipment["quantity"],
                shipment["shipment_date"],
                shipment["expected_delivery_date"],
            ),
        )

    def get_transaction_by_id(self, transaction_id):
        connection = sqlite3.connect(self.db_name)
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM transactions WHERE id = ?", (transaction_id,))
        transaction = cursor.fetchone()
        connection.close()
        return transaction


# Initialize the database object
db = SupplyChainDatabase()

# Call the function to create the database
db.create_database()
