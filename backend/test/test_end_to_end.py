import httpx
import pytest

BASE_URL = "https://backend-production-05cd.up.railway.app"

def test_e2e_docs_accessible():
    response = httpx.get(f"{BASE_URL}/docs")
    assert response.status_code == 200
    assert "Swagger UI" in response.text

def test_e2e_predict_valid():
    payload = {
        "LotArea": 9000,
        "OverallQual": 6,
        "YearBuilt": 2001,
        "Neighborhood": "NAmes"
    }
    response = httpx.post(f"{BASE_URL}/predict", json=payload)
    assert response.status_code in [200, 400]  

def test_e2e_predict_invalid():
    payload = {
        "LotArea": "invalid",
        "OverallQual": 7,
        "YearBuilt": 2005,
        "Neighborhood": "NAmes"
    }
    response = httpx.post(f"{BASE_URL}/predict", json=payload)
    assert response.status_code == 422
