## Supply Chain Predictor

The `supply_chain_ml.py` file contains the `SupplyChainPredictor` class which is used for predicting the quantity of transactions in the supply chain. This class uses a linear regression model for predictions.

### Key Methods

1. `__init__(self, db_file, target_column)`: Initializes the `SupplyChainPredictor` with the SQLite database file and the target column name.

2. `load_data(self)`: Loads and cleans the data from the SQLite database.

3. `prepare_data(self, df)`: Prepares the data for training the model. It splits the data into training and testing sets.

4. `train_model(self)`: Trains the linear regression model on the data.

5. `evaluate_model(self)`: Evaluates the model using Mean Squared Error, Mean Absolute Error, and R^2 score.

6. `save_model(self, file_format='pkl')`: Saves the trained model in different formats (pickle, joblib, ONNX).

### Usage

```python
# Initialize SupplyChainPredictor
predictor = SupplyChainPredictor(db_file='supply_chain.db', target_column='trans_quantity')

# Load and prepare data
data = predictor.load_data()
predictor.prepare_data(data)

# Train the model
predictor.train_model()

# Evaluate the model
predictor.evaluate_model()

# Save the model in different formats
predictor.save_model(file_format='pkl')
predictor.save_model(file_format='joblib')
predictor.save_model(file_format='onnx')
```

