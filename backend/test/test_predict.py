import pytest
from fastapi.testclient import TestClient
from app import app

client = TestClient(app)

def test_prediction_success():
    response = client.post(
        "/predict",
        json={
            "LotArea": 8500,
            "OverallQual": 7,
            "YearBuilt": 2005,
            "Neighborhood": "NAmes"
        }
    )
    # En test mode, on s'attend à une erreur car le modèle est None
    assert response.status_code == 400
    assert response.json()["detail"] == "Model is not loaded (test mode)"

def test_prediction_invalid_input():
    response = client.post(
        "/predict",
        json={
            "LotArea": "invalid",
            "OverallQual": 7,
            "YearBuilt": 2005,
            "Neighborhood": "NAmes"
        }
    )
    assert response.status_code == 422  