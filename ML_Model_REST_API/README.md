# ML Model REST API

**Status:** 🚀 Completed  
**Tech Stack:** Python, FastAPI, Uvicorn, Scikit-learn (RandomForest), Pydantic

## Overview
This project bridges the gap between a static Machine Learning notebook and a production-ready software system. It demonstrates how to take a trained `RandomForestRegressor` (predicting California housing prices) and deploy it as a high-performance REST API. 

By wrapping the model in FastAPI, external applications (like a web app or mobile app) can send HTTP POST requests containing housing features, and the server will return real-time price predictions in JSON format.

## Setup & Installation

```Bash
Install the required dependencies:
```

```Bash
pip install -r requirements.txt
Train the Model (Optional, if you want to generate a fresh .joblib file):
```
```Bash
python train.py
Run the API Server:
```
```Bash
uvicorn main:app --reload
Test the API:
```

Open your browser and navigate to the auto-generated Swagger UI docs: http://127.0.0.1:8000/docs

Expand the /predict POST endpoint.

Click "Try it out" and hit "Execute" to send a test request and view the model's prediction.

## Architecture & Flow
1. **Model Training (`train.py`):** * Loads the California Housing Dataset.
   * Trains a `RandomForestRegressor` on 5 specific features (Median Income, House Age, Avg Rooms, Avg Bedrooms, Population).
   * Serializes (saves) the trained model into a `.joblib` file so it doesn't need to be retrained on every API call.
2. **Data Validation (Pydantic):** * Defines a strict data schema using Pydantic's `BaseModel`. This ensures the API rejects malformed requests (e.g., passing a string instead of a float for "House Age") before they crash the model.
3. **API Endpoint (`main.py`):** * Loads the serialized model into memory upon server startup.
   * Exposes a `/predict` POST endpoint. It converts the incoming validated JSON data into a Pandas DataFrame, passes it to the model, and returns the predicted median house value.
