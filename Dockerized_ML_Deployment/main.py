# main.py

from fastapi import FastAPI
import joblib
from pydantic import BaseModel
import numpy as np

# 1. Create a FastAPI app instance
app = FastAPI(title="California Housing Price Predictor")

# 2. Load the trained model
model = joblib.load('housing_model.pkl')

# 3. Define the request body structure using Pydantic
# These are the features our model was trained on.
class HousingFeatures(BaseModel):
    MedInc: float
    HouseAge: float
    AveRooms: float
    AveBedrms: float
    Population: float
    AveOccup: float
    Latitude: float
    Longitude: float

# 4. Define the prediction endpoint
@app.post("/predict", tags=["Predictions"])
async def predict_price(features: HousingFeatures):
    
    # Convert the input data from the request into a NumPy array
    # The order of features must be the same as during training!
    data = np.array([[
        features.MedInc,
        features.HouseAge,
        features.AveRooms,
        features.AveBedrms,
        features.Population,
        features.AveOccup,
        features.Latitude,
        features.Longitude
    ]])

    # Make a prediction
    # The output is a price in units of 100,000 USD
    prediction = model.predict(data)[0]

    # Return the prediction
    return {"predicted_median_value": f"${prediction * 100000:.2f}"}

# Root endpoint
@app.get("/", tags=["General"])
async def read_root():
    return {"message": "Welcome to the California Housing Price Predictor API!"}