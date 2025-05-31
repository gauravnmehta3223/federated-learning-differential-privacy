# server.py
import flwr as fl
import numpy as np
import tensorflow as tf  # or import torch

# Define a simple model
def create_model():
    model = tf.keras.Sequential([
        tf.keras.layers.Dense(64, activation='relu', input_shape=(32,)),  # Example input shape
        tf.keras.layers.Dense(10, activation='softmax')
    ])
    model.compile(optimizer='adam', loss='sparse_categorical_crossentropy', metrics=['accuracy'])
    return model

# Create a Flower server
class CustomServer(fl.server.Server):
    def __init__(self):
        super().__init__()
        self.global_model = create_model()

    def aggregate_fit(self, results):
        # Aggregate weights from clients
        weights = [result[1] for result in results]
        new_weights = np.mean(weights, axis=0)
        self.global_model.set_weights(new_weights)

# Start the server
if __name__ == "__main__":
    fl.server.start_server(server_address="127.0.0.1:9090", config={"num_rounds": 5})