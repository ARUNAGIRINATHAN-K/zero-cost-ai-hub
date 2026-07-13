import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.datasets import fetch_california_housing
import joblib

print("Starting the training script...")

housing = fetch_california_housing()
X = pd.DataFrame(housing.data, columns=housing.feature_names)
y = pd.Series(housing.target, name='MedHouseVal')

print("Dataset loaded successfully.")

features_to_use = ['MedInc', 'HouseAge', 'AveRooms', 'AveBedrms', 'Population']
X = X[features_to_use]

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)
print("Data split into training and testing sets.")

model = RandomForestRegressor(n_estimators=100, random_state=42)
print("Training the RandomForestRegressor model...")
model.fit(X_train, y_train)
print("Model training complete.")

model_filename = 'california_housing_model.joblib'
joblib.dump(model, model_filename)

print(f"Model saved as {model_filename}. Training script finished.")