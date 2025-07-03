import os
import pandas as pd
import joblib
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

# Initialisation du modèle
model = None
model_path = os.path.join(os.path.dirname(__file__), "model.pkl")

if os.path.exists(model_path):
    try:
        model = joblib.load(model_path)
        print("✅ Model loaded successfully.")
    except Exception as e:
        print("❌ ERROR loading model:", e)
        raise RuntimeError(f"Could not load model: {e}")
else:
    print("❌ model.pkl not found. Model will not be loaded.")

# Définition des données d’entrée
class HouseFeatures(BaseModel):
    LotArea: float
    OverallQual: int
    YearBuilt: int
    Neighborhood: str

app = FastAPI()

origins = ["*"]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/predict")
def predict_price(features: HouseFeatures):
    global model
    try:
        if model is None:
            raise ValueError("Model is not loaded")
        input_df = pd.DataFrame([features.dict()])
        prediction = model.predict(input_df)
        return {"estimated_price": float(prediction[0])}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
