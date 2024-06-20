"""Very similar to unit tests, instead of using built-in fastapi TestClient I will use requests."""

import os

import pytest
import requests

BASE_URL = os.environ.get("BASE_URL", "http://localhost:8000")


@pytest.fixture(scope="function")
def placed_order():
    response = requests.post(
        f"{BASE_URL}/orders", json={"ticker": "TEST", "amount": 100, "order_type": "BUY"}
    )
    assert response.status_code == 200
    order_id = response.json()["orderId"]
    yield order_id
    # Clean up: Delete the order after the test completes
    requests.delete(f"{BASE_URL}/orders/{order_id}")


def test_create_order():
    response = requests.post(
        f"{BASE_URL}/orders", json={"ticker": "TEST", "amount": 100, "order_type": "BUY"}
    )
    assert response.status_code == 200
    json_response = response.json()
    assert "orderId" in json_response
    assert json_response["status"] == "PENDING"


def test_get_orders(placed_order):
    response = requests.get(f"{BASE_URL}/orders")
    assert response.status_code == 200


def test_get_order(placed_order):
    response = requests.get(f"{BASE_URL}/orders/{placed_order}")
    assert response.status_code == 200
    json_response = response.json()
    assert json_response["id"] == placed_order


def test_delete_order(placed_order):
    response = requests.delete(f"{BASE_URL}/orders/{placed_order}")
    assert response.status_code == 200
    deleted_response = requests.get(f"{BASE_URL}/orders/{placed_order}")
    assert deleted_response.json().get("status") == "CANCELLED"


def test_delete_invalid_id():
    response = requests.delete(f"{BASE_URL}/orders/invalid")
    assert response.status_code == 404


def test_invalid_order_fetch():
    response = requests.get(f"{BASE_URL}/orders/invalid_id")
    assert response.status_code == 404
