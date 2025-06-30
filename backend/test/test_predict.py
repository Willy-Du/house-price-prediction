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
    assert response.status_code == 200
    assert "estimated_price" in response.json()
    assert isinstance(response.json()["estimated_price"], float)

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