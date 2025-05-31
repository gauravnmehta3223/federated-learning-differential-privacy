# Federated Learning with Differential Privacy

This project implements a federated learning system with differential privacy using the Flower library. The system is designed to train a neural network model on distributed healthcare data while preserving privacy through differential privacy mechanisms.

## Project Overview

The project implements a client-server architecture where:
- A central server coordinates the federated learning process
- Multiple clients (10 in this implementation) train the model on their local data
- Differential privacy is applied to protect sensitive information during the training process

## Dataset

The project uses a healthcare dataset containing the following features:
- ABP Diastolic
- ABP Systolic
- Glucose
- Heart Rate
- Respiratory Rate
- Temperature (°F)
- hospital_expire_flag (target variable)

The dataset contains 71,026 rows of patient data.

## Project Structure

```
.
├── data/
│   └── merged_data.csv
├── server.py
├── client.py
├── start_clients.sh
├── requirements.txt
└── README.md
```

## Requirements

- Python 3.7+
- Flower (flwr)
- TensorFlow
- Pandas
- NumPy

## Installation

1. Clone the repository:
```bash
git clone https://github.com/Gmehta604/Differential-Privacy-Federated-Learning.git
```

2. Install the required packages:
```bash
pip install -r requirements.txt
```

## Usage

1. Start the server:
```bash
python server.py
```

2. Start the clients (in a new terminal):
```bash
./start_clients.sh
```

## Implementation Details

### Server
- Coordinates the federated learning process
- Aggregates model updates from clients
- Implements differential privacy mechanisms

### Clients
- Each client receives a portion of the dataset
- Trains the model locally
- Applies differential privacy to model updates
- Sends encrypted updates to the server

### Differential Privacy
The implementation includes differential privacy mechanisms to protect sensitive data during the federated learning process.

## Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgments

- Flower library for federated learning implementation
- TensorFlow for neural network implementation
- Contributors and maintainers of the project
