import os
import pandas as pd
import mlflow.pyfunc
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

# Initialisation du modèle
model = None

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

# ❌ Ne surtout pas garder ce bloc TESTING
# if os.getenv("TESTING") == "1":
#     model = None

# ✅ Chargement du vrai modèle
if os.path.exists("/mlruns"):
    run_dir = "/mlruns/671704907248415465"
else:
    run_dir = "../mlruns/671704907248415465"

runs = sorted([
    d for d in os.listdir(run_dir)
    if os.path.isdir(os.path.join(run_dir, d)) and d != "models"
])

if not runs:
    raise RuntimeError(f"No MLflow runs found in {run_dir}")

latest_run = runs[-1]

models_dir = os.path.join(run_dir, "models")
if not os.path.exists(models_dir):
    raise RuntimeError(f"No 'models' directory found in {run_dir}")

model_ids = sorted([
    d for d in os.listdir(models_dir)
    if os.path.isdir(os.path.join(models_dir, d))
])

if not model_ids:
    raise RuntimeError(f"No model versions found in {models_dir}")

latest_model_id = model_ids[-1]
model_path = os.path.join(models_dir, latest_model_id, "artifacts")

print("====== DEBUG: Model loading path check ======")
print("Current working directory:", os.getcwd())
print("Checking path:", model_path)
print("Exists:", os.path.exists(model_path))
print("==============================================")

try:
    model = mlflow.pyfunc.load_model(model_path)
    print("✅ Model loaded successfully.")
except Exception as e:
    print("❌ ERROR loading model:", e)
    raise RuntimeError(f"Could not load model: {e}")

@app.post("/predict")
def predict_price(features: HouseFeatures):
    global model
    try:
        if model is None:
            raise ValueError("Model is not loaded (test mode)")
        input_df = pd.DataFrame([features.dict()])
        prediction = model.predict(input_df)
        return {"estimated_price": float(prediction[0])}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))