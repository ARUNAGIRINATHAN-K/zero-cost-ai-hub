from fastapi import FastAPI
from pydantic import BaseModel
import joblib
import pandas as pd

app = FastAPI(title="California Housing Price Prediction API")

model = joblib.load('california_housing_model.joblib')

class HouseFeatures(BaseModel):
    MedInc: float      # Median income in block group
    HouseAge: float    # Median house age in block group
    AveRooms: float    # Average number of rooms per household
    AveBedrms: float   # Average number of bedrooms per household
    Population: float  # Block group population
    
    class Config:
        schema_extra = {
            "example": {
                "MedInc": 8.3252,
                "HouseAge": 41.0,
                "AveRooms": 6.9841,
                "AveBedrms": 1.0238,
                "Population": 322.0
            }
        }

@app.post("/predict")
def predict_price(features: HouseFeatures):
    """
    Predicts the median house value based on input features.
    """
    input_data = pd.DataFrame([features.dict()])
    
    prediction = model.predict(input_data)
    
    predicted_value = prediction[0]
    
    return {"predicted_median_house_value": predicted_value}

@app.get("/")
def read_root():
    return {"message": "Welcome to the Housing Price Prediction API!"}