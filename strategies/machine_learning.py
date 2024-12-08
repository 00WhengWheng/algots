import os
import pandas as pd
import importlib
from ..utils.base_strategy import BaseStrategy
from sklearn.model_selection import train_test_split

class MachineLearning(BaseStrategy):
    def __init__(self, features: list, target: str = 'Signal', model_name: str = None):
        super().__init__()
        self.features = features
        self.target = target
        self.model_name = model_name
        self.model = None
        if model_name:
            self.load_model(model_name)
    required_patterns = []

    @staticmethod
    def list_available_models():
        data_dir = os.path.join(os.path.dirname(__file__), '..', '..', 'data')
        model_files = [f for f in os.listdir(data_dir) if f.endswith('_model.py')]
        models = [f.replace('_model.py', '').capitalize() for f in model_files]
        return models
    def load_model(self, model_name):
        try:
            module = importlib.import_module(f"data.{model_name.lower()}_model")
            model_class = getattr(module, f"{model_name}Model")
            self.model = model_class()
            self.model_name = model_name
        except (ImportError, AttributeError):
            raise ValueError(f"Model {model_name} not found or not properly implemented.")

    def train_and_predict(self, data: pd.DataFrame) -> pd.DataFrame:
        if self.model is None:
            raise ValueError("No model selected. Please choose a model before training.")

        if not set(self.features).issubset(data.columns):
            missing_features = set(self.features) - set(data.columns)
            raise ValueError(f"Missing required features: {missing_features}")

        if self.target not in data.columns:
            raise ValueError(f"Missing required target column: {self.target}")

        train_data, test_data = train_test_split(data, test_size=0.2, shuffle=False)

        X_train, y_train = train_data[self.features], train_data[self.target]
        X_test = test_data[self.features]

        self.model.train(X_train, y_train)

        test_data['Predicted_Signal'] = self.model.predict(X_test)

        return pd.concat([train_data, test_data], ignore_index=True)

    def generate_signals(self, data: pd.DataFrame) -> pd.DataFrame:
        if self.model is None:
            raise ValueError("No model selected. Please choose a model before generating signals.")

        data_with_predictions = self.train_and_predict(data)

        # You can customize this part based on how you want to interpret the predictions
        data_with_predictions['Signal'] = data_with_predictions['Predicted_Signal']

        return data_with_predictions