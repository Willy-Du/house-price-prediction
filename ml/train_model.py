import os
import pathlib
import pandas as pd
import numpy as np
import mlflow
import mlflow.sklearn
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_absolute_error
from sklearn.preprocessing import OneHotEncoder
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.impute import SimpleImputer
import joblib

mlruns_path = pathlib.Path(__file__).parent.parent / "mlruns"
mlruns_uri = mlruns_path.as_uri()
os.environ["MLFLOW_TRACKING_URI"] = mlruns_uri
print("MLflow tracking URI:", mlruns_uri)

df = pd.read_csv("data/train.csv")

features = ["LotArea", "OverallQual", "YearBuilt", "Neighborhood"]
target = "SalePrice"

df = df[features + [target]].dropna()

X = df[features]
y = df[target]

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

numeric_features = ["LotArea", "OverallQual", "YearBuilt"]
categorical_features = ["Neighborhood"]

numeric_transformer = SimpleImputer(strategy="mean")
categorical_transformer = Pipeline([
    ("imputer", SimpleImputer(strategy="most_frequent")),
    ("onehot", OneHotEncoder(handle_unknown="ignore"))
])

preprocessor = ColumnTransformer([
    ("num", numeric_transformer, numeric_features),
    ("cat", categorical_transformer, categorical_features)
])

model = Pipeline([
    ("preprocessor", preprocessor),
    ("regressor", RandomForestRegressor(n_estimators=100, random_state=42))
])

mlflow.set_experiment("house-price-estimation")

with mlflow.start_run():
    model.fit(X_train, y_train)
    predictions = model.predict(X_test)
    mae = mean_absolute_error(y_test, predictions)

    # Log metrics et modèle
    mlflow.log_metric("MAE", mae)
    mlflow.sklearn.log_model(model, "model", registered_model_name="house-price-model")

    print(f"MAE: {mae:.2f}")


joblib.dump(model, "backend/model.pkl")
