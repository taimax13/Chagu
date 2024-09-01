import tensorflow as tf
from tensorflow.keras import layers, models

class AnomalyDetectionModel:
    def __init__(self, input_shape):
        self.model = self.build_model(input_shape)

    def build_model(self, input_shape):
        model = models.Sequential([
            layers.Dense(64, activation='relu', input_shape=(input_shape,)),
            layers.Dense(32, activation='relu'),
            layers.Dense(16, activation='relu'),
            layers.Dense(1, activation='sigmoid')
        ])
        model.compile(optimizer='adam', loss='binary_crossentropy', metrics=['accuracy'])
        return model

    def train(self, X_train, y_train, epochs=10, batch_size=32, validation_split=0.2):
        history = self.model.fit(X_train, y_train, epochs=epochs, batch_size=batch_size, validation_split=validation_split)
        return history

    def evaluate(self, X_test, y_test):
        loss, accuracy = self.model.evaluate(X_test, y_test)
        return loss, accuracy

# Example usage:
# anomaly_model = AnomalyDetectionModel(X_train.shape[1])
# history = anomaly_model.train(X_train, y_train)
# loss, accuracy = anomaly_model.evaluate(X_test, y_test)
# print(f'Test Accuracy: {accuracy:.4f}')
