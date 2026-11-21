from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_home():
    response = client.get("/")

    assert response.status_code == 200
    assert response.json()["status"] == "Application Running"

def test_orders():
    response = client.get("/orders")

    assert response.status_code == 200