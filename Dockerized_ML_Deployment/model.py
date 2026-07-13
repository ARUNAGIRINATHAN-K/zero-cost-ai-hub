# model.py

from sklearn.ensemble import GradientBoostingRegressor
from sklearn.datasets import fetch_california_housing
import joblib

def train_and_save_model():    
    print("Loading data and training the model...")

    # 1. Load the California Housing dataset
    housing = fetch_california_housing()
    X, y = housing.data, housing.target

    # 2. Initialize and train the model
    # We're using Gradient Boosting, a powerful ensemble method for regression.
    # The parameters here are just examples; in a real project, you'd tune them.
    model = GradientBoostingRegressor(n_estimators=100, learning_rate=0.1, max_depth=3)
    model.fit(X, y)

    # 3. Save the trained model to a file
    joblib.dump(model, 'housing_model.pkl')

    print("Model trained and saved as housing_model.pkl!")
    print("Feature names:", housing.feature_names) # To help us with testing later

if __name__ == "__main__":
    train_and_save_model()