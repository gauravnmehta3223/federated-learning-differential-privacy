# client.py
import flwr as fl
import numpy as np
import pandas as pd
import tensorflow as tf  # or import torch

# Define a simple model
def create_model():
    model = tf.keras.Sequential([
        tf.keras.layers.Dense(64, activation='relu', input_shape=(6,)),  # 6 features
        tf.keras.layers.Dense(1, activation='sigmoid')  # Binary classification
    ])
    model.compile(optimizer='adam', loss='binary_crossentropy', metrics=['accuracy'])
    return model

# Load local data from CSV
def load_data(file_path):
    data = pd.read_csv(file_path)
    # Drop rows with missing values
    data = data.dropna()
    # Features and labels
    X = data[['ABP Diastolic', 'ABP Systolic', 'Glucose', 'Heart Rate', 'Respiratory Rate', 'Temperature (°F)']].values
    y = data['hospital_expire_flag'].values
    return X, y

# Create a Flower client
class CustomClient(fl.client.NumPyClient):
    def __init__(self, file_path):
        self.model = create_model()
        self.data, self.labels = load_data(file_path)

    def get_parameters(self):
        return self.model.get_weights()

    def fit(self, parameters, config):
        self.model.set_weights(parameters)
        self.model.fit(self.data, self.labels, epochs=1, verbose=0)
        return self.model.get_weights(), len(self.data), {}

    def evaluate(self, parameters, config):
        self.model.set_weights(parameters)
        loss, accuracy = self.model.evaluate(self.data, self.labels, verbose=0)
        return loss, len(self.data), {"accuracy": accuracy}

# Start the client
if __name__ == "__main__":
    file_path = "data/merged_data.csv"  # Path to your CSV file
    fl.client.start_numpy_client(server_address="127.0.0.1:9090", client=CustomClient(file_path))