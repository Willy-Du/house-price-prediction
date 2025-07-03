import pytest
import sys
import os
from fastapi.testclient import TestClient

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app import app

client = TestClient(app)

# ---------- UNIT TESTS ----------

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

def test_missing_field():
    response = client.post(
        "/predict",
        json={
            "LotArea": 8500,
            "OverallQual": 7,
            "YearBuilt": 2005
            # Missing Neighborhood
        }
    )
    assert response.status_code == 422

# ---------- INTEGRATION TESTS ----------

def test_integration_valid_data():
    response = client.post("/predict", json={
        "LotArea": 10000,
        "OverallQual": 8,
        "YearBuilt": 1995,
        "Neighborhood": "CollgCr"
    })
    assert response.status_code in [200, 400]

def test_integration_boundary_values():
    response = client.post("/predict", json={
        "LotArea": 1,
        "OverallQual": 1,
        "YearBuilt": 1900,
        "Neighborhood": "OldTown"
    })
    assert response.status_code in [200, 400]

def test_integration_unusual_neighborhood():
    response = client.post("/predict", json={
        "LotArea": 5000,
        "OverallQual": 5,
        "YearBuilt": 2010,
        "Neighborhood": "ImaginaryPlace999"
    })
    assert response.status_code in [200, 400]
