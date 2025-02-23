"""
End-to-end tests simulating real-world scenarios.
Tests include:
- Health endpoint check.
- Data retrieval endpoint test.
"""

from fastapi.testclient import TestClient
from src.services.api.routes import app

client = TestClient(app)

def test_health_endpoint():
    response = client.get("/health")
    assert response.status_code == 200
    json_data = response.json()
    assert "status" in json_data and json_data["status"] == "ok", "Health endpoint did not return expected status."

def test_sample_data_endpoint():
    response = client.get("/api/data")
    assert response.status_code == 200
    json_data = response.json()
    assert "fleet_id" in json_data, "Response should contain fleet_id."

if __name__ == "__main__":
    import pytest
    pytest.main()
