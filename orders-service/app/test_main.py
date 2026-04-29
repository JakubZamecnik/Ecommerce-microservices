from fastapi.testclient import TestClient
from .main import app

client = TestClient(app)

def test_read_root():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"status": "online", "service": "Orders"}

def test_create_invalid_order():
    # Testujeme naši novou validaci na záporné množství
    payload = {
        "customer_id": 1,
        "product_name": "Test",
        "quantity": -5
    }
    response = client.post("/orders/", json=payload)
    assert response.status_code == 422
    assert "quantity" in response.text
