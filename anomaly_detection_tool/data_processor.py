import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder, StandardScaler

class DataProcessor:
    def __init__(self, csv_file):
        self.data = pd.read_csv(csv_file)
        self.label_encoders = {}
        self.scaler = StandardScaler()

    def preprocess_data(self):
        for column in ['IP', 'Hostnames', 'OS']:
            self.label_encoders[column] = LabelEncoder()
            self.data[column] = self.label_encoders[column].fit_transform(self.data[column].astype(str))

        self.data['Port'] = self.scaler.fit_transform(self.data[['Port']])
        self.data['Timestamp'] = pd.to_datetime(self.data['Timestamp']).astype(int) / 10**9
        return self.data

    def get_features_and_labels(self, label_column='Anomaly'):
        if label_column not in self.data.columns:
            raise ValueError(f"Label column '{label_column}' not found in data.")

        X = self.data.drop([label_column], axis=1)
        y = self.data[label_column]
        return X, y

    def split_data(self, X, y, test_size=0.2, random_state=42):
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=test_size, random_state=random_state)
        return X_train, X_test, y_train, y_test

# # Example usage:
# processor = DataProcessor('shodan_scan_results.csv')
# processed_data = processor.preprocess_data()
# X, y = processor.get_features_and_labels()
# X_train, X_test, y_train, y_test = processor.split_data(X, y)
