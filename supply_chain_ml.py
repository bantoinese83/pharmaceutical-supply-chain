import pickle
import sqlite3

import joblib
import onnx
import pandas as pd
from skl2onnx import convert_sklearn
from skl2onnx.common.data_types import FloatTensorType
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error, mean_absolute_error, r2_score
from sklearn.model_selection import cross_val_score
from sklearn.model_selection import train_test_split


class SupplyChainPredictor:
    def __init__(self, db_file, target_column):
        self.db_file = db_file
        self.target_column = target_column
        self.features_train = None
        self.features_test = None
        self.target_train = None
        self.target_test = None
        self.model = None

    def load_data(self):
        conn = sqlite3.connect(self.db_file)
        query = """
            SELECT transactions.quantity AS trans_quantity, inventory.quantity AS inventory_quantity, 
                   suppliers.name AS supplier_name, customers.name AS customer_name, 
                   products.product_id, products.name AS product_name, products.description, 
                   products.price, shipments.shipment_date, shipments.expected_delivery_date
            FROM transactions
            JOIN suppliers ON transactions.supplier_id = suppliers.id
            JOIN customers ON transactions.customer_id = customers.id
            JOIN products ON transactions.product_id = products.product_id
            JOIN inventory ON transactions.product_id = inventory.product_id
            JOIN shipments ON transactions.id = shipments.id
        """
        df = pd.read_sql_query(query, conn)
        conn.close()

        # Data cleaning
        print(df)  # Print DataFrame before cleaning
        df['trans_quantity'] = pd.to_numeric(df['trans_quantity'], errors='coerce')
        print(df)  # Print DataFrame after converting 'trans_quantity' to numeric
        df['inventory_quantity'] = pd.to_numeric(df['inventory_quantity'], errors='coerce')
        print(df)  # Print DataFrame after converting 'inventory_quantity' to numeric
        df['price'] = pd.to_numeric(df['price'], errors='coerce')
        print(df)  # Print DataFrame after converting 'price' to numeric
        df['shipment_date'] = pd.to_datetime(df['shipment_date'])
        print(df)  # Print DataFrame after converting 'shipment_date' to datetime
        df['expected_delivery_date'] = pd.to_datetime(df['expected_delivery_date'])
        print(df)  # Print DataFrame after converting 'expected_delivery_date' to datetime
        df['shipment_duration'] = (df['expected_delivery_date'] - df['shipment_date']).dt.days
        print(df)  # Print DataFrame after calculating 'shipment_duration'
        df.drop(['shipment_date', 'expected_delivery_date'], axis=1, inplace=True)
        print(df)  # Print DataFrame after dropping 'shipment_date' and 'expected_delivery_date'
        df.fillna(0, inplace=True)
        print(df)  # Print DataFrame after filling missing values

        # Fill missing values with a default value (e.g., 0 for numeric columns)
        df.fillna(0, inplace=True)

        if df.empty:
            raise ValueError("The DataFrame is empty after data cleaning")

        if self.target_column not in df.columns:
            raise ValueError(f"Column '{self.target_column}' not found in DataFrame")

        return df

    def prepare_data(self, df):
        numeric_columns = df.select_dtypes(include=['int64', 'float64']).columns
        if self.target_column in numeric_columns:
            self.features_train, self.features_test, self.target_train, self.target_test = \
                train_test_split(df[numeric_columns].drop(self.target_column, axis=1), df[self.target_column],
                                 test_size=0.2, random_state=42)
        else:
            raise ValueError(f"Column '{self.target_column}' not found in DataFrame")

    def train_model(self):
        self.model = LinearRegression()
        self.model.fit(self.features_train, self.target_train)

    def evaluate_model(self):
        predictions = self.model.predict(self.features_test)
        mse = mean_squared_error(self.target_test, predictions)
        mae = mean_absolute_error(self.target_test, predictions)
        r2 = r2_score(self.target_test, predictions)
        print(f"Mean Squared Error: {mse}")
        print(f"Mean Absolute Error: {mae}")
        print(f"R^2 Score: {r2}")

    def save_model(self, file_format='pkl'):
        if file_format not in ['pkl', 'joblib', 'onnx']:
            raise ValueError("Invalid file format. Choose one of: 'pkl', 'joblib', 'onnx'")

        if file_format == 'pkl':
            with open('model/psct.pkl', 'wb') as f:
                pickle.dump(self.model, f)
        elif file_format == 'joblib':
            joblib.dump(self.model, 'model/psct.joblib')
        elif file_format == 'onnx':
            initial_type = [('float_input', FloatTensorType([None, self.features_train.shape[1]]))]
            onnx_model = convert_sklearn(self.model, initial_types=initial_type)
            onnx.save_model(onnx_model, 'model/psct.onnx')

        print(f"Model saved as 'model.{file_format}'")


if __name__ == "__main__":
    # Initialize SupplyChainPredictor
    predictor = SupplyChainPredictor(db_file='supply_chain.db', target_column='trans_quantity')

    try:
        # Load and prepare data
        data = predictor.load_data()
        predictor.prepare_data(data)

        # Train the model
        predictor.train_model()

        # Perform cross-validation
        scores = cross_val_score(predictor.model, predictor.features_train, predictor.target_train, cv=5)

        # Print the scores
        print('Cross-validation scores: ', scores)

        # Print the average score
        print('Average cross-validation score: ', scores.mean())

        # Evaluate the model
        predictor.evaluate_model()

        # Save the model in different formats
        predictor.save_model(file_format='pkl')
        predictor.save_model(file_format='joblib')
        predictor.save_model(file_format='onnx')

    except Exception as e:
        print("An error occurred:", e)
