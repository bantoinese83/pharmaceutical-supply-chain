# Pharmaceutical Supply Chain Tracking API

## Overview

This project provides a simple API for tracking pharmaceutical products throughout the supply chain using a combination of a blockchain ledger and a relational database. The API is built using Flask and Flask-RESTx and it integrates SQLite for data storage and validation using the Voluptuous library.

## Features

- Record and track transactions in the pharmaceutical supply chain.
- Store transactions in both a blockchain and a relational database.
- Retrieve the entire blockchain for verification and audit purposes.
- Data validation for all API inputs.

## Technologies

- **Flask**: A micro web framework written in Python.
- **Flask-RESTx**: An extension for Flask that adds support for quickly building REST APIs.
- **SQLite**: A C library that provides a lightweight, disk-based database.
- **Voluptuous**: A Python library for validating data.

## Getting Started

### Prerequisites

Ensure you have the following installed:

- Python 3.7+
- Pip (Python package installer)

### Installation

1. Clone the repository:

    ```sh
    git clone https://github.com/bantoinese83/pharmaceutical-supply-chain.git
    cd pharmaceutical-supply-chain
    ```

2. Create a virtual environment:

    ```sh
    python -m venv venv
    source venv/bin/activate  # On Windows use `venv\Scripts\activate`
    ```

3. Install the required packages:

    ```sh
    pip install -r requirements.txt
    ```

### Database Setup

Before running the application, you need to set up the SQLite database:

```sh
python db.py
```

This will create the necessary tables in the supply_chain.db database file.

### Running the Application

To start the Flask application, run the following command:

```sh
flask run --port=8000 --host=localhost
```

The application will be accessible at `http://localhost:5000`.

## API Reference

The API documentation is available at `http://localhost:5000/api/doc`.

### Endpoints

## API Endpoints

### /blockchain/transaction (POST)

Record a new transaction in the supply chain.

**Request Body**

```json
{
  "product_id": "123456",
  "transaction_detail": "Purchase",
  "supplier_id": 1,
  "customer_id": 2,
  "quantity": 100,
  "shipment_date": "2021-01-01",
  "expected_delivery_date": "2021-01-10"
}

```

**Response:**

```json
{
  "message": "Transaction added successfully"
}
```

### /blockchain/chain (GET)

Retrieve the entire blockchain.

**Response:**

```json
{
  "length": 2,
  "chain": [
    {
      "index": 0,
      "timestamp": 1625212345,
      "data": "Genesis Block",
      "hash": "5f4dcc3b5aa765d61d8327deb882cf99",
      "previous_hash": "0"
    },
    {
      "index": 1,
      "timestamp": 1625212445,
      "data": {
        "product_id": "123456",
        "transaction_detail": "Purchase",
        "supplier_id": 1,
        "customer_id": 2,
        "quantity": 100,
        "shipment_date": "2021-01-01",
        "expected_delivery_date": "2021-01-10"
      },
      "hash": "9b74c9897bac770ffc029102a200c5de",
      "previous_hash": "5f4dcc3b5aa765d61d8327deb882cf99"
    }
  ]
}

```

### /blockchain/transactions (GET)

Retrieve all transactions from the relational database.

**Response:**

```json
{
  "transactions": [
    {
      "id": 1,
      "product_id": "123456",
      "transaction_detail": "Purchase",
      "supplier_id": 1,
      "customer_id": 2,
      "quantity": 100,
      "shipment_date": "2021-01-01",
      "expected_delivery_date": "2021-01-10"
    }
  ]
}
```
## API Endpoints (continued)

1. **Create Transaction**
   - **Endpoint:** `/blockchain/create_transaction` (POST)
   - **Description:** This endpoint is used to record a new transaction in the supply chain.

2. **Get Chain**
   - **Endpoint:** `/blockchain/get_chain` (GET)
   - **Description:** This endpoint is used to retrieve the entire blockchain.

3. **Get Block by Index**
   - **Endpoint:** `/blockchain/get_block_by_index/<int:index>` (GET)
   - **Description:** This endpoint is used to retrieve a block by its index.

4. **Get Block by Hash**
   - **Endpoint:** `/blockchain/get_block_by_hash/<string:hash>` (GET)
   - **Description:** This endpoint is used to retrieve a block by its hash.

5. **Get Transaction by ID**
   - **Endpoint:** `/transactions/transactions/<int:id>` (GET)
   - **Description:** This endpoint is used to retrieve a transaction by its ID.

6. **Create Supplier**
   - **Endpoint:** `/supplier/create_supplier` (POST)
   - **Description:** This endpoint is used to add a new supplier.

7. **Create Customer**
   - **Endpoint:** `/customer/create_customer` (POST)
   - **Description:** This endpoint is used to add a new customer.

8. **Get All Products**
   - **Endpoint:** `/products/get_all_products` (GET)
   - **Description:** This endpoint is used to retrieve all products.

9. **Get Product by ID**
   - **Endpoint:** `/products/get_product_by_id/<int:id>` (GET)
   - **Description:** This endpoint is used to retrieve a product by its ID.

10. **Get All Inventory**
   - **Endpoint:** `/inventory/get_all_inventory` (GET)
   - **Description:** This endpoint is used to retrieve all inventory.

11. **Get Inventory by Product ID**
   - **Endpoint:** `/inventory/get_inventory_by_product_id/<int:product_id>` (GET)
   - **Description:** This endpoint is used to retrieve inventory by product ID.

12. **Create Shipment**
   - **Endpoint:** `/shipments/create_shipment` (POST)
   - **Description:** This endpoint is used to add a new shipment.

13. **Get All Transactions**
   - **Endpoint:** `/transactions/get_all_transactions` (GET)
   - **Description:** This endpoint is used to retrieve all transactions.



Error Handling

The API provides a global error handler for unexpected exceptions, returning a 500 Internal Server Error with a generic message.

Validation

The API validates all inputs using the Voluptuous library:

- `product_id`: Must be a string of exactly six digits.
- `transaction_detail`: Must be a non-empty string.
- `supplier_id` and `customer_id`: Must be non-negative integers.
- `quantity`: Must be a non-negative integer.
- `shipment_date` and `expected_delivery_date`: Must be valid dates in `YYYY-MM-DD` format.


## Machine Learning Component

The project includes a machine learning component for predicting the quantity of transactions in the supply chain. This is implemented in the `SupplyChainPredictor` class in the `supply_chain_ml.py` file.

### Features
- Load and prepare data from the SQLite database.
- Train a linear regression model on the data.
- Evaluate the model using Mean Squared Error, Mean Absolute Error, and R^2 score.
- Save the trained model in different formats (pickle, joblib, ONNX).

### Usage

1. **Initialize the `SupplyChainPredictor`** with the SQLite database file and the target column name:
    ```python
    predictor = SupplyChainPredictor(db_file='supply_chain.db', target_column='trans_quantity')
    ```

2. **Load and prepare the data:**
    ```python
    data = predictor.load_data()
    predictor.prepare_data(data)
    ```

3. **Train the model:**
    ```python
    predictor.train_model()
    ```

4. **Evaluate the model:**
    ```python
    predictor.evaluate_model()
    ```

5. **Save the model:**
    ```python
    predictor.save_model(file_format='pkl')
    predictor.save_model(file_format='joblib')
    predictor.save_model(file_format='onnx')
    ```

### Prerequisites

The following Python packages are required:

- `scikit-learn`
- `pandas`
- `joblib`
- `skl2onnx`
- `onnx`

These can be installed using pip:
```sh
pip install scikit-learn pandas joblib skl2onnx onnx
```

