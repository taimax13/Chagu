# Anomaly Detection Model
## Overview
This repository contains a Python class AnomalyDetectionModel built using TensorFlow and Keras
for detecting anomalies in network traffic data. The class encapsulates the creation, training,
and evaluation of a neural network model designed to classify network data as either normal or anomalous.

### Why Use a Sequential Model?
The Sequential model in Keras is a simple, linear stack of layers. 
It is ideal for building feedforward neural networks where the model 
progresses through each layer sequentially, without any branching or complex topologies.

### Key Reasons for Using Sequential:

Simplicity: The Sequential API is straightforward and easy to use. It is perfect for beginners and 
for models that involve a single input and output with layers stacked one after the other.

Linear Stack: For the task of anomaly detection, the architecture typically involves a simple
forward pass through several dense layers, making the Sequential model a natural fit.

Flexibility: While simple, the Sequential model is flexible enough to allow for customization
through the addition of various types of layers, activation functions, and regularization techniques.

Example Usage
```python

# Initialize the model with the input shape
anomaly_model = AnomalyDetectionModel(X_train.shape[1])

# Train the model
history = anomaly_model.train(X_train, y_train)

# Evaluate the model on the test data
loss, accuracy = anomaly_model.evaluate(X_test, y_test)
print(f'Test Accuracy: {accuracy:.4f}')
```

Dependencies
Python 3.x
TensorFlow
Keras (included with TensorFlow)
Scikit-learn
Pandas
Installation
Install the required packages using pip:

Conclusion
The Sequential model is a great choice for this anomaly detection task due to its simplicity,
ease of use, and the linear nature of the problem. This approach ensures that the model is easy
to build, understand, and maintain while still providing robust performance for binary classification
tasks such as anomaly detection.